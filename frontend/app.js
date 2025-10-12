// Global state for the cart
let cart = {}; // { itemId: { name, price, quantity }, ... }

// --- On Page Load ---
window.onload = () => {
    loadMenu();
    loadOrders();
};

// --- Menu Functions ---
async function loadMenu() {
    try {
        const response = await fetch('/api/menu');
        if (!response.ok) throw new Error('Failed to load menu');
        const menuItems = await response.json();

        const menuContainer = document.getElementById('menu-container');
        menuContainer.innerHTML = ''; // Clear existing menu

        menuItems.forEach(item => {
            const div = document.createElement('div');
            div.className = 'menu-item';
            div.innerHTML = `
                <span>${item.name} - $${item.price.toFixed(2)}</span>
                <button onclick='addToCart(${JSON.stringify(item)})'>Add</button>
            `;
            menuContainer.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading menu:', error);
        alert('Could not load menu.');
    }
}

// --- Cart Functions ---
function addToCart(item) {
    if (cart[item.id]) {
        cart[item.id].quantity++;
    } else {
        cart[item.id] = {
            name: item.name,
            price: item.price,
            quantity: 1
        };
    }
    updateCartView();
}

function updateCartView() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalContainer = document.getElementById('cart-total');
    cartItemsContainer.innerHTML = '';
    let total = 0;

    for (const id in cart) {
        const item = cart[id];
        const li = document.createElement('li');
        li.textContent = `${item.name} x ${item.quantity} - $${(item.price * item.quantity).toFixed(2)}`;
        cartItemsContainer.appendChild(li);
        total += item.price * item.quantity;
    }

    cartTotalContainer.textContent = `Total: $${total.toFixed(2)}`;
}

async function submitOrder() {
    const items = Object.keys(cart).map(id => ({
        id: parseInt(id),
        quantity: cart[id].quantity
    }));

    if (items.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to submit order');
        }

        alert('Order submitted successfully!');
        cart = {}; // Clear the cart
        updateCartView();
        loadOrders(); // Refresh the orders list
    } catch (error) {
        console.error('Error submitting order:', error);
        alert(`Error: ${error.message}`);
    }
}

// --- Kitchen/Order Functions ---
async function loadOrders() {
    try {
        const response = await fetch('/api/orders');
        if (!response.ok) throw new Error('Failed to load orders');
        const orders = await response.json();

        const ordersContainer = document.getElementById('orders-container');
        ordersContainer.innerHTML = ''; // Clear existing list

        orders.forEach(order => {
            const card = document.createElement('div');
            card.className = 'order-card';
            
            const itemsHtml = order.items.map(item => 
                `<li>${item.name} x ${item.quantity}</li>`
            ).join('');

            card.innerHTML = `
                <h3>Order #${order.id}</h3>
                <p>Status: <span class="status status-${order.status.replace('_', '-')}">${order.status}</span></p>
                <p>Total: $${order.total_price.toFixed(2)}</p>
                <p>Items:</p>
                <ul class="order-items-list">${itemsHtml}</ul>
                <div>
                    Change Status:
                    <button onclick="updateOrderStatus(${order.id}, 'pending')">Pending</button>
                    <button onclick="updateOrderStatus(${order.id}, 'in_progress')">In Progress</button>
                    <button onclick="updateOrderStatus(${order.id}, 'completed')">Completed</button>
                </div>
            `;
            ordersContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading orders:', error);
        alert('Could not load orders.');
    }
}

async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`/api/orders/${orderId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });

        if (!response.ok) throw new Error('Failed to update status');
        
        loadOrders(); // Refresh the view
    } catch (error) {
        console.error('Error updating status:', error);
        alert('Could not update order status.');
    }
}

// Export functions for testing if in a Node.js environment (like Jest)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { addToCart, updateCartView, cart };
}