# Current State Specification & Flowchart

This document outlines the current architecture and request flow of the 3-Tier POS Web Application.

## Architecture Flowchart

The following flowchart illustrates the interaction between the different components of the application when a user makes a request to an API endpoint (e.g., fetching the menu).

```mermaid
graph TD
    subgraph "User's Device"
        A[Browser]
    end

    subgraph "Frontend Tier (Served by Nginx)"
        B(Nginx Server)
    end

    subgraph "Backend Tier (Python)"
        C(Flask/Gunicorn API)
    end

    subgraph "Database Tier (PostgreSQL)"
        D[(PostgreSQL Database)]
    end

    A -- "1. User action triggers API call (e.g., GET /api/menu)" --> B
    B -- "2. Nginx acts as reverse proxy, forwards request" --> C
    C -- "3. Flask app receives request and executes logic" --> C
    C -- "4. Queries the database" --> D
    D -- "5. Returns data rows" --> C
    C -- "6. Formats data as JSON and sends response" --> B
    B -- "7. Forwards HTTP response to browser" --> A
    A -- "8. JavaScript renders the data on the page" --> A
```