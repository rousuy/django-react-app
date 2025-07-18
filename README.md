# Django REST + React Vite Web Application

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-REST-092E20?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-20-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

---

> Architecture combining Django REST, React (Vite), and Docker.  
> Developed with the assistance of generative AI tools (Amazon Q)
> integrated into the development environment (VSCode),
> contributing to the README documentation, frontend design, and initial test scaffolding.

---

## Overview

Stacks used:

- **Django REST Framework** as the API backend  
- **React + Vite** for the frontend  
- **Docker Compose** for containerized development and deployment  
- **Celery + RabbitMQ** for asynchronous task processing

---

## Architecture

```plain-text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  React UI   │────▶│  Django API │────▶│ PostgreSQL  │
│  (Vite)     │     │  (REST)     │     │ Database    │
│             │     │             │     │             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐     ┌─────────────┐
                    │             │     │             │
                    │  Celery     │◀───▶│  RabbitMQ   │
                    │  Workers    │     │  Broker     │
                    │             │     │             │
                    └─────────────┘     └─────────────┘
```

## Features

### 🔧 Backend

- Python 3.12, Django REST
- `uv` for dependency management
- `ruff` (lint/format) + `pyright` (type checking)

### ⚛️ Frontend

- React 18 + TypeScript
- Vite for fast builds
- Component-based design

### 🚀 DevOps

- Multi-stage Docker builds
- Compose environments for dev and prod
- `.env` per service

---

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker + Compose](https://docs.docker.com/compose/) — Compose v2 is included in Docker v20.10.13+
- [Make (optional)](https://www.gnu.org/software/make/) — install via package manager, e.g.  
  - macOS: `brew install make`  
  - Ubuntu/Debian: `sudo apt install make`  
  - Windows: use [Chocolatey](https://chocolatey.org/packages/make) ou [WSL](https://learn.microsoft.com/windows/wsl/)

### Option 1: Using Make (Recommended)

```bash
git clone https://github.com/yourusername/django-react-architecture.git
cd django-react-architecture

make help       # List available commands
make env-setup  # Setup .env files
make up         # Start dev environment
```

### Option 2: Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/yourusername/django-react-architecture.git
cd django-react-architecture

# Setup environment variables
chmod +x scripts/setup_envs.sh
./scripts/setup_envs.sh

# Start development environment with file watching
docker compose -f compose.dev.yml --env-file ./api/.env --env-file ./ui/.env up --build --watch
```

### Access Points

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- API Documentation: http://localhost:8000/api/docs/

### Project Structure

```plain-text
/
├── api/                        
│   ├── config/                    # Core Django settings and ASGI/Wsgi application
│   ├── src/                      # Main source code: apps, serializers, views, etc.
│   ├── manage.py                 # Django's command-line utility
│   └── pyproject.toml            # Python dependencies and build configuration
│
├── ui/                          
│   ├── public/                   # Static public assets
│   ├── src/                      # React source code
│   ├── index.html                # HTML entry point
│   └── package.json              # Node.js dependencies and scripts
│
├── compose.dev.yml               # Docker Compose configuration for development
├── compose.prod.yml              # Docker Compose configuration for production
└── Makefile                       # Common developer tasks (build, up, lint, etc.)
```

### Development Workflow examples

```bash
# View all available commands
make help

# Run tests
make api-test

# Format code lint and check types
make api-all-check
```

## Production Deployment

The project includes production-ready Docker configurations with:

- Multi-stage builds for minimal image sizes
- Environment-specific optimizations
- Static file serving configuration

## License

MIT
]]
>