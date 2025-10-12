// Import functions from app.js
// Note: You might need to adjust app.js to export functions for testing,
// for example by adding `module.exports = { addToCart, ... };` at the end of the file.
// For now, we assume they are globally available in the test environment.

const { addToCart, updateCartView, cart } = require('./app');

describe('Frontend POS Logic', () => {

    beforeEach(() => {
        // Reset the cart and DOM before each test
        for (const key in cart) {
            delete cart[key];
        }
        document.body.innerHTML = `
            <ul id="cart-items"></ul>
            <div id="cart-total"></div>
        `;
    });

    test('addToCart should add a new item to the cart', () => {
        const burger = { id: 1, name: 'Classic Burger', price: 12.99 };
        
        addToCart(burger);

        expect(cart[1]).toBeDefined();
        expect(cart[1].quantity).toBe(1);
        expect(cart[1].name).toBe('Classic Burger');
    });

    test('addToCart should increment quantity for an existing item', () => {
        const burger = { id: 1, name: 'Classic Burger', price: 12.99 };
        
        addToCart(burger); // First add
        addToCart(burger); // Second add

        expect(cart[1].quantity).toBe(2);
    });

});
