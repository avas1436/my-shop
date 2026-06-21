# ShopVerse

A comprehensive, high-performance e-commerce platform built with a microservices-inspired architecture. This project delivers a modern, responsive user interface with native Right-to-Left (RTL) support, powered by a robust dual-backend system designed for scalability and speed.

## Key Features

- Unified User Interface: A seamless, responsive design featuring distinct environments for the public storefront and an advanced administrative dashboard.
- Dual-Engine Backend Architecture: Strategically combines the rapid development and ecosystem of Python (FastAPI) with the raw performance, memory safety, and concurrency of Rust (Axum).
- Advanced Catalog Management: Comprehensive systems for product categorization, dynamic inventory tracking, media galleries, and advanced search filtration.
- Secure Authentication: Implementation of One-Time Password (OTP) flows and robust Role-Based Access Control (RBAC).
- Containerized Infrastructure: Fully isolated, reproducible, and easily deployable environments utilizing Docker, with Traefik serving as an intelligent edge router and reverse proxy.

## Technology Stack

### Frontend Architecture

- Vue.js 3
- Axios
- Tailwind CSS
- Vite
- Pinia

### Primary Backend Service (Python)

- Framework: FastAPI
- Database ORM & Migrations: SQLAlchemy, Alembic
- Asynchronous Task Queue: Celery
- Caching: Redis
- Database: PostgreSQL

### High-Performance Service (Rust)

- Framework: Axum
- Caching: Redis
- Database Integration: PostgreSQL

### DevOps & Infrastructure

- Containerization: Docker & Docker Swarm
- Reverse Proxy & Load Balancing: Traefik
- Web Server: Caddy

## Project Structure

```text
├── Axum/       # Rust-based service optimized for performance-critical read operations.
├── FastAPI/    # Primary Python service managing user authentication, cart logic, product workflows, and background tasks.
├── frontend/   # Vue.js application containing both the storefront and the administrative control panel.
├── docker/     # Container configurations, Traefik dynamic routing, and middleware definitions.
└── stack.yml   # Primary Docker Swarm configuration file orchestrating the entire platform.
```

## Prerequisites

To run this project locally, ensure you have the following installed on your system (an Ubuntu/Linux environment is recommended):

- Docker

To run the services locally for development:

- Cargo
- UV
- pnpm

## Installation and Setup

1. Clone the repository:
   git clone <your-repository-url>
   cd <your-project-directory>

2. Configure Environment Variables:
   Duplicate the provided settings files within their respective directories (FastAPI, Axum, frontend) and rename them to .env. Populate these files with your specific database credentials, secret keys, and API endpoints.

3. Deploy the Infrastructure:
   Initialize the containers using Docker Swarm:

docker compose -f stack.yml up -d

4. Access the Services:

Frontend Application: http://localhost:3000 (or the port defined in your web server configuration)

FastAPI Documentation (Swagger UI): http://localhost:8000/docs

Axum API Endpoints: Refer to the docs/openapi.rs routing definitions.

5. Author

Developed by Amir Abbas Abbaszadeh
