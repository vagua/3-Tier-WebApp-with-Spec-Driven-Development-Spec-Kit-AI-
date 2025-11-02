# Current State Specification & Flowchart

This document outlines the current architecture and request flow of the 3-Tier POS Web Application.

## Architecture Flowchart

The following flowchart illustrates the interaction between the different components of the application when a user makes a request to an API endpoint (e.g., fetching the menu).

```mermaid
graph TD
    subgraph "User's Device"
        A[Browser]
    end

    subgraph "Manager Node (Windows WSL)"
        B1[Frontend Service (Nginx)]
        B2[Backend Service (Flask/Gunicorn)]
    end

    subgraph "Worker Node (Lab VM)"
        C[(PostgreSQL Database)]
    end

    A -- "1. User action triggers API call (GET /api/menu, POST /api/order)" --> B1
    B1 -- "2. Nginx forwards request to backend service via overlay network" --> B2
    B2 -- "3. Backend executes business logic" --> B2
    B2 -- "4. Queries database on Worker node via overlay network" --> C
    C -- "5. Returns rows (menu/order info)" --> B2
    B2 -- "6. Formats data as JSON and responds" --> B1
    B1 -- "7. Forwards HTTP response to browser" --> A
    A -- "8. Browser renders UI" --> A
```