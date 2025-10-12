from flask import Flask, request, jsonify
import psycopg2, os, json, time

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "namesdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

def init_db_connection():
    """
    Establishes a database connection with retry logic.
    This is crucial for Docker Compose startup order.
    """
    retries = 10  # Increase retries for more robustness
    delay = 5     # seconds
    while retries > 0:
        try:
            conn = get_conn()
            cur = conn.cursor()
            # Check if the main table from init.sql exists.
            cur.execute("SELECT 1 FROM menu_items LIMIT 1;")
            cur.close()
            conn.close()
            print("Database is ready and table 'menu_items' exists.")
            return
        except psycopg2.OperationalError as e:
            # This catches connection errors (e.g., DB not up yet)
            print(f"Database connection failed: {e}")
        except psycopg2.errors.UndefinedTable:
            # This catches the specific error when the table doesn't exist yet
            print("Database is up, but 'menu_items' table not found. Waiting for init.sql to complete.")
        
        retries -= 1
        print(f"Retrying in {delay} seconds... ({retries} retries left)")
        time.sleep(delay)
    raise Exception("Could not connect to the database or find 'menu_items' table after several retries.")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

@app.route("/names", methods=["GET"])
def get_names():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM names ORDER BY id;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([{"id": r[0], "name": r[1], "created_at": r[2]} for r in rows])

@app.route("/api/menu", methods=["GET"])
def get_menu():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM menu_items ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Convert price from Decimal to float for JSON serialization
    menu_items = [{"id": r[0], "name": r[1], "price": float(r[2])} for r in rows]
    return jsonify(menu_items)

@app.route("/api/names", methods=["POST"])
def add_name():
    data = request.get_json()
    name = data.get("name", "").strip()
    if not name or len(name) > 50:
        return jsonify({"error": "Invalid name"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO names (name) VALUES (%s) RETURNING id;", (name,))
    new_id = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": new_id, "name": name}), 201

@app.route("/api/names/<int:name_id>", methods=["DELETE"])
def delete_name(name_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM names WHERE id = %s;", (name_id,))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "deleted"}), 200

@app.route("/api/health", methods=["GET"])
def health():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close(); conn.close()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500
    
@app.route("/api/orders", methods=["GET"])
def get_orders():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, items, total_price, status, created_at FROM orders ORDER BY created_at DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    orders = [{
        "id": r[0], 
        "items": r[1], 
        "total_price": float(r[2]), 
        "status": r[3],
        "created_at": r[4]
    } for r in rows]
    return jsonify(orders)


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    item_ids_and_quantities = data.get("items", []) # e.g., [{"id": 1, "quantity": 2}]

    if not item_ids_and_quantities:
        return jsonify({"error": "Order must contain items"}), 400

    conn = get_conn()
    cur = conn.cursor()

    try:
        # Fetch prices from DB to prevent price tampering
        item_ids = [item['id'] for item in item_ids_and_quantities]
        cur.execute("SELECT id, name, price FROM menu_items WHERE id = ANY(%s);", (item_ids,))
        menu_items_from_db = {r[0]: {"name": r[1], "price": float(r[2])} for r in cur.fetchall()}

        total_price = 0
        order_items = []
        for item_data in item_ids_and_quantities:
            item_id = item_data['id']
            quantity = item_data['quantity']
            if item_id not in menu_items_from_db:
                raise ValueError(f"Invalid menu item ID: {item_id}")
            
            price = menu_items_from_db[item_id]['price']
            total_price += price * quantity
            order_items.append({
                "id": item_id,
                "name": menu_items_from_db[item_id]['name'],
                "price": price,
                "quantity": quantity
            })

        cur.execute(
            "INSERT INTO orders (items, total_price) VALUES (%s, %s) RETURNING id;",
            (json.dumps(order_items), total_price)
        )
        new_order_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": new_order_id, "status": "pending"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route("/api/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    new_status = data.get("status")
    # Add validation for status if needed
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = %s WHERE id = %s;", (new_status, order_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "updated"})

if __name__ == "__main__":
    init_db_connection()
    app.run(host="0.0.0.0", port=8000)
