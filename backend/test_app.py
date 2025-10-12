import pytest
import json
import os
import psycopg2
from app import app as flask_app, get_conn

# --- Test Database Setup ---

@pytest.fixture(scope='module')
def test_db():
    """
    Fixture to set up the test database.
    It creates the necessary tables and yields a connection.
    After tests are done, it tears down the tables.
    """
    conn = get_conn()
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            items JSONB NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    yield conn

    # Teardown: drop tables
    cur.execute("DROP TABLE IF EXISTS menu_items, orders;")
    conn.commit()
    cur.close()
    conn.close()

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Here you could override config for testing, e.g., using a test DB
    yield flask_app

# --- Test Client Fixture ---

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}

def test_get_menu(client, test_db):
    """Test the /api/menu endpoint."""
    # Setup: Insert some mock data for this test
    cur = test_db.cursor()
    cur.execute("INSERT INTO menu_items (name, price) VALUES (%s, %s), (%s, %s);",
                ('Test Burger', 9.99, 'Test Fries', 3.50))
    test_db.commit()

    # Execute
    response = client.get('/api/menu')

    # Assert
    assert response.status_code == 200
    menu_items = response.get_json()
    assert isinstance(menu_items, list)
    assert len(menu_items) > 0  # Check that the menu is not empty
    assert 'name' in menu_items[0]
    assert 'price' in menu_items[0]
    assert menu_items[0]['name'] == 'Test Burger'

    # Teardown: Clean up the mock data
    cur.execute("TRUNCATE TABLE menu_items;")
    test_db.commit()
    cur.close()

def test_create_and_get_orders(client, test_db):
    """Test creating a new order and then getting all orders."""
    cur = test_db.cursor()
    # Setup: Ensure tables are clean and we have menu items
    cur.execute("TRUNCATE TABLE menu_items, orders RESTART IDENTITY;")
    cur.execute("INSERT INTO menu_items (name, price) VALUES (%s, %s) RETURNING id;",
                ('Test Pizza', 15.00))
    item_id = cur.fetchone()[0]
    test_db.commit()

    # 1. Test POST /api/orders
    order_payload = {
        "items": [{"id": item_id, "quantity": 2}]
    }
    post_response = client.post('/api/orders', json=order_payload)
    assert post_response.status_code == 201
    post_data = post_response.get_json()
    assert 'id' in post_data
    assert post_data['status'] == 'pending'

    # 2. Test GET /api/orders
    get_response = client.get('/api/orders')
    assert get_response.status_code == 200
    orders_list = get_response.get_json()
    assert isinstance(orders_list, list)
    assert len(orders_list) == 1
    
    order = orders_list[0]
    assert order['id'] == post_data['id']
    assert order['total_price'] == 30.00 # 15.00 * 2
    assert len(order['items']) == 1
    assert order['items'][0]['name'] == 'Test Pizza'

    # Teardown
    cur.execute("TRUNCATE TABLE menu_items, orders RESTART IDENTITY;")
    test_db.commit()
    cur.close()

def test_update_order_status(client, test_db):
    """Test updating an order's status."""
    cur = test_db.cursor()
    # Setup: Create a menu item and an order
    cur.execute("TRUNCATE TABLE menu_items, orders RESTART IDENTITY;")
    cur.execute("INSERT INTO menu_items (name, price) VALUES ('Test Drink', 2.50);")
    cur.execute("INSERT INTO orders (items, total_price, status) VALUES (%s, %s, %s) RETURNING id;",
                (json.dumps([{"id": 1, "name": "Test Drink", "quantity": 1}]), 2.50, 'pending'))
    order_id = cur.fetchone()[0]
    test_db.commit()

    # Execute PUT request
    update_payload = {"status": "completed"}
    put_response = client.put(f'/api/orders/{order_id}', json=update_payload)
    assert put_response.status_code == 200

    # Verify the change
    cur.execute("SELECT status FROM orders WHERE id = %s;", (order_id,))
    updated_status = cur.fetchone()[0]
    assert updated_status == "completed"

    # Teardown
    cur.execute("TRUNCATE TABLE menu_items, orders RESTART IDENTITY;")
    test_db.commit()
    cur.close()

def test_create_order_error_scenarios(client, test_db):
    """Test error scenarios for order creation."""
    cur = test_db.cursor()
    cur.execute("TRUNCATE TABLE menu_items, orders RESTART IDENTITY;")
    test_db.commit()

    # Scenario 1: Submit an empty order
    empty_payload = {"items": []}
    response_empty = client.post('/api/orders', json=empty_payload)
    assert response_empty.status_code == 400
    assert "Order must contain items" in response_empty.get_json()['error']

    # Scenario 2: Submit an order with an invalid menu item ID
    invalid_item_payload = {
        "items": [{"id": 999, "quantity": 1}] # 999 is an invalid ID
    }
    response_invalid = client.post('/api/orders', json=invalid_item_payload)
    assert response_invalid.status_code == 500 # Based on current implementation
    assert "Invalid menu item ID: 999" in response_invalid.get_json()['error']

    cur.close()