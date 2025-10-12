# Quick Start Guide

This guide provides the minimal, copy-pastable steps to get the 3-Tier POS Web Application running on your local machine.

### Prerequisites

Ensure you have the following installed:
-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)

> **Note:** You do not need to install Node.js, PostgreSQL, or other runtime environments on your machine. Docker will handle the setup for all services, including the database.

---

### Step 1: Clone the Repository

Open your terminal and clone the project repository.

```bash
git clone https://github.com/vagua/3-Tier-WebApp-with-Spec-Driven-Development-Spec-Kit-AI-.git
```
*(Note: Replace the URL with your actual repository URL)*

### Step 2: Navigate to the Project Directory

```bash
cd 3-Tier-WebApp-with-Spec-Driven-Development-Spec-Kit-AI-
```
*(Note: Replace with your actual repository folder name)*

### Step 3: Build and Run the Application

Use Docker Compose to build all images and start the services in detached mode.

```bash
docker-compose up --build -d
```

### Step 4: Access the Application

Wait a moment for the services to initialize. Once ready, open your web browser and navigate to:

`http://localhost:8080`

### Step 5: Stop the Application

When you are finished, you can stop all running services with the following command:

```bash
docker-compose down
```