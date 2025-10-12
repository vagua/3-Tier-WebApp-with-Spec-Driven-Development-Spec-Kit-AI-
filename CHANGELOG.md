# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

## [1.0.0] - 2025-10-12

### Added
-   **Initial Application Setup**: Established a 3-tier architecture using Docker Compose.
    -   Frontend: Nginx serving static HTML, CSS, and JavaScript.
    -   Backend: Flask/Gunicorn API for business logic.
    -   Database: PostgreSQL for data persistence.
-   **POS Core Features**:
    -   API endpoints to get menu (`GET /api/menu`), get orders (`GET /api/orders`), create an order (`POST /api/orders`), and update order status (`PUT /api/orders/:id`).
    -   Frontend UI to display the menu, add items to a cart, submit orders, and view all orders in a "kitchen" view.
-   **Testing**:
    -   Backend unit tests using Pytest, covering all API endpoints including success and error cases.
    -   Frontend unit test setup using Jest.
-   **Documentation**:
    -   `README.md` with project overview and instructions.
    -   `QUICKSTART.md` for fast setup and execution.
    -   `CONTRIBUTING.md` outlining contribution guidelines.
    -   `LICENSE` file with the MIT License.