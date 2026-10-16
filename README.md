# Polylang-Blog

A multi-language blog application framework implemented across different programming languages (Python, PHP, and JavaScript), supported by a robust containerized infrastructure utilizing Docker Compose, MySQL, Redis, Meilisearch, and RabbitMQ.

---

## Architecture & Design Patterns

The project follows strict software engineering principles to ensure maintainability and separation of concerns:
- **`MVC` (Model-View-Controller)** pattern for application flow and clean routing.
- **`Repository` Pattern** for isolated database operations (MySQL 8.0) with robust empty-result checks.
- **`Service` Pattern** for encapsulating core business logic and background orchestration.
- **`Command / Worker` Pattern** for handling scheduled tasks and asynchronous queue jobs.
- **`Infrastructure-First Approach`**: Fully containerized environment ensuring parity between local development and production.

---

## Current Implementation Status

| Component | Status | Description |
| :--- | :--- | :--- |
| **Infrastructure (Docker)** | **Completed** | Nginx reverse proxy, MySQL, Redis, RabbitMQ, Meilisearch, Mailcatcher, and Admin UI panels are fully operational. |
| **Python / Flask Implementation** | **In Progress** | Core architecture, routing, database hydrators, repositories, frontend views, and backend Admin panel (`My Posts`, `My Comments`, Post/Comment management) are active. |
| **PHP Implementation** | **Not Started** | Scheduled for future development using the same architectural blueprint. |
| **JavaScript (Node.js) Implementation** | **Not Started** | Scheduled for future development using the same architectural blueprint. |

---

## Infrastructure & Services (Docker Compose)

The environment runs via Docker Compose and includes the following stack:
- **`nginx`**: Reverse proxy handling SSL termination and multi-app routing via wildcard certificates.
- **`python`**: Python 3.13 service running Flask 3.x.
- **`php`**: PHP 8.2 service (pending implementation).
- **`js`**: Node.js 24 service (pending implementation).
- **`mysql`**: MySQL 8.0 relational database with initialization schemas.
- **`redis` & `redis-commander`**: Session management, caching layer, and web UI.
- **`rabbitmq`**: Message broker for asynchronous background jobs (e.g., email notifications).
- **`meilisearch`**: Full-text search engine synced with post management.
- **`mailer` (Mailcatcher)**: Captures outgoing application emails during development.
- **`adminer`**: Web-based database management interface.

---

## Infrastructure Roadmap: Dedicated CDN Container

To optimize static asset delivery across multiple language implementations (Python, PHP, JS), the architecture is transitioning toward a dedicated **CDN container**:
- **Shared Volume Strategy**: Applications will upload media assets (such as post images and attachments) and static assets (CSS/JS files like TinyMCE) into a shared Docker volume.
- **Dedicated Hosting**: A lightweight Nginx-based CDN container will independently serve these static files.
- **Cross-App Access**: All language implementations (`python`, `php`, `js`) will reference the centralized CDN endpoint for asset loading, ensuring optimal caching and clean separation of concerns.

---

## Project Structure

```text
.
├── CONSPECT.md                 # Detailed functional and technical specification
├── README.md                   # Project overview and status
├── docker-compose.yml          # Container orchestration configuration
├── Makefile                    # Automation shortcuts (SSL generation, container management)
├── mysql/                      # Database initialization scripts and schemas
├── nginx/                      # Nginx configurations (vhosts per app/service) & SSL certs
└── www/                        # Application source code directories
    ├── js/                     # JavaScript implementation (Not Started)
    ├── php/                    # PHP implementation (Not Started)
    └── python/                 # Python/Flask implementation (In Progress)
        ├── app/                # Core application logic (controllers, models, repositories, views)
        ├── requirements.txt    # Python dependencies
        └── run.py              # Application entry point

```

---

## Quick Start Guide

1. **Generate Local SSL Certificates**:
```bash
make ssl

```


2. **Start Core Infrastructure Services**:
```bash
make up-initials

```


3. **Start the Python Application Service**:
```bash
make up-python

```


4. **Access the Application**:
* Configure local host entries or use your wildcard setup to access the Python app at `https://python.localhost`.
* Access database management via Adminer and background queues via respective service dashboards.
