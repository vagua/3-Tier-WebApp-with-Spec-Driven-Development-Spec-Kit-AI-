# Future Works

This document outlines potential features and improvements that can be added to the project in the future.

## 1. User Authentication & Roles

To make the system more secure and suitable for a real-world business environment.

-   **Implementation**:
    -   Add a `users` table to the database for storing user credentials (with hashed passwords).
    -   Create backend endpoints for user registration, login (`/api/login`), and logout. Use JWT (JSON Web Tokens) for session management.
    -   Develop a frontend login page.
-   **Advanced**:
    -   Introduce user roles like `cashier` and `manager`.
    -   Implement role-based access control (RBAC) on the backend to restrict certain actions (e.g., only managers can view reports or edit the menu).

## 2. Real-time Updates & Notifications

To improve the user experience of the kitchen view by providing real-time order updates without needing a manual refresh.

-   **Implementation**:
    -   Integrate WebSockets (e.g., using `Flask-SocketIO` on the backend).
    -   When a new order is created or an existing order's status is updated, the backend will broadcast an event to all connected kitchen view clients.
    -   The frontend will listen for these WebSocket events and automatically refresh the order list.

## 3. Inventory Management

-   **Implementation**:
    -   Add a `stock` column to the `menu_items` table to track the quantity of each item.
    -   Update the order creation logic to check for sufficient stock before confirming an order.
    -   Disable the "Add" button on the frontend for out-of-stock items.

## 4. Reporting & Analytics

-   **Implementation**:
    -   Create new backend API endpoints to generate sales reports (e.g., `GET /api/reports/daily-sales`, `GET /api/reports/popular-items`).
    -   Add a new "Reports" page to the frontend.
    -   Use a charting library (like `Chart.js`) to visualize the report data, such as daily revenue or top-selling products.