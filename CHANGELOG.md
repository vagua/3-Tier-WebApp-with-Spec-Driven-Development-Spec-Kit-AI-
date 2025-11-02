# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added 2025-11-2
- **Distributed Deployment (Docker Swarm)**:
  - `swarm/stack.yaml` added for multi-node production-like deployment.
  - Overlay network for service-to-service traffic.
  - Placement constraints:
    - Database (`db`) runs only on lab node (Worker VM).  
    - Backend (`backend`) and Frontend (`frontend`) run on Manager node.
  - Ingress publish: Frontend exposed on port 80 of Manager node.
  - Persistent volume for DB on Worker node.
- **Ops Scripts**:
  - `ops/init-swarm.sh`: Initialize Swarm, configure Manager & Worker roles, print join token.
  - `ops/deploy.sh`: Deploy stack to Swarm.
  - `ops/verify.sh`: Verify service status, DB tables, and sample data.
  - `ops/cleanup.sh`: Remove stack and persistent volumes for clean redeploy.
- **Documentation / Evidence**:
  - `docs/EVIDENCE.md` created with command output and screenshots.
  - Short demo video (≤5 min) showing end-to-end deployment & verification.
- **Improved Compose File**:
  - `compose.yaml` unchanged but verified for local single-host development.

### Changed
- Updated architecture flowchart in `spec/` to reflect distributed Swarm topology and service placement.
- Added sample menu initialization and volume handling to support Swarm deployment.

## [1.0.0] - 2025-10-12

### Added
- **Initial Application Setup**: Established a 3-tier architecture using Docker Compose.
  - Frontend: Nginx serving static HTML, CSS, and JavaScript.
  - Backend: Flask/Gunicorn API for business logic.
  - Database: PostgreSQL for data persistence.
- **POS Core Features**:
  - API endpoints to get menu (`GET /api/menu`), get orders (`GET /api/orders`), create an order (`POST /api/orders`), and update order status (`PUT /api/orders/:id`).
  - Frontend UI to display the menu, add items to a cart, submit orders, and view all orders in a "kitchen" view.
- **Testing**:
  - Backend unit tests using Pytest, covering all API endpoints including success and error cases.
  - Frontend unit test setup using Jest.
- **Documentation**:
  - `README.md` with project overview and instructions.
  - `QUICKSTART.md` for fast setup and execution.
  - `CONTRIBUTING.md` outlining contribution guidelines.
  - `LICENSE` file with the MIT License.
- **Single-host Compose Deployment**:
  - `compose.yaml` verified for local development.
