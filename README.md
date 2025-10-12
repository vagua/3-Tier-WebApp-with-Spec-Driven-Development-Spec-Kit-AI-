# 3-Tier POS Web Application

This repo is a practice project which is co-oped with ai assistant include Gemini Pro 2.5(Vscode Gemini Code Assist)/ ChatGPT GPT-5 free version.
This is a simple 3-tier web application that functions as a basic Point-of-Sale (POS) system. It allows users to view a menu, add items to a cart, submit orders, and view the status of submitted orders in a "kitchen" view.

This project is built using a spec-driven development (SDD) approach and is licensed under the MIT License.

## How It Works

The application follows a classic 3-tier architecture:

-   **Frontend**: A static web interface built with HTML, CSS, and vanilla JavaScript, served by an **Nginx** web server. It provides the user interface for placing and viewing orders.
-   **Backend**: A RESTful API built with **Flask** (a Python web framework) and run by **Gunicorn**. It handles business logic, such as calculating order totals and interacting with the database.
-   **Database**: A **PostgreSQL** database that persists all menu items and order information.

### Request/Response Flow

1.  **User Interaction**: The user opens the web page, and the frontend fetches menu items from the backend via a `GET /api/menu` request.
2.  **API Gateway (Nginx)**: The Nginx container acts as a reverse proxy. It serves the static frontend files (HTML, JS, CSS) and forwards any requests with a `/api/` prefix to the backend service.
3.  **Business Logic (Backend)**: The Flask application receives the API request.
    -   For `GET /api/menu`, it queries the PostgreSQL database for all menu items.
    -   When an order is submitted (`POST /api/orders`), it validates the data, calculates the total price, and inserts a new record into the `orders` table in the database.
4.  **Data Persistence (Database)**: The PostgreSQL container stores all data. It uses a Docker volume (`db_data`) to ensure that data is not lost even if the container is removed.

## How to Run

### Prerequisites

-   Docker
-   Docker Compose

### Running the Application

1.  Clone this repository to your local machine.
2.  Navigate to the project's root directory in your terminal.
3.  Run the following command to build the Docker images and start all services:

    ```bash
    docker-compose up --build
    ```

4.  Once all services are up and running, open your web browser and navigate to:

    `http://localhost:8080`

You should see the POS application interface.

## How to Test

This project includes separate unit tests for the backend and frontend, which can be run via Docker Compose.

### Backend Tests

To run the Python (Pytest) unit tests for the backend API:

```bash
docker-compose run --rm backend pytest
```

### Frontend Tests

To run the JavaScript (Jest) unit tests for the frontend logic:

```bash
docker-compose run --rm frontend npm test
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.