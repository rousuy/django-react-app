# ============================== Django + React PoC Makefile ===========================
# Development workflow automation for Django REST API + React frontend
# Includes: Dependency management, testing, and database operations

# ============================== Configuration Variables ===============================
# Django management command with uv
UV_MANAGE := python manage.py

# Testing configurations
PYTEST_FAST := pytest -v --tb=short
PYTEST_COV := pytest --cov=api --cov-report=term-missing --cov-report=html

# Docker Compose setup for development environment
DC := docker compose -f compose.dev.yml --env-file ./api/.env --env-file ./ui/.env
EXEC := $(DC) exec
RUN := $(DC) run --rm
RUN_NO_TTY := $(RUN) -T

# Service definitions matching compose.dev.yml
SERVICES := react_ui django_api database message_broker celery_worker

# ================================= Default Target ===================================
.DEFAULT_GOAL := help 

# Display comprehensive help with all available commands
help:
	@echo "🚀 Django + React PoC Development Commands"
	@echo ""
	@echo "📦 Environment Management:"
	@echo "    env-setup                     - Set up all 'envs' required for the project to work"
	@echo "    build                         - Build and start all services from scratch"
	@echo "    up                            - Start all services (database, api, ui, celery)"
	@echo "    down                          - Stop all services and cleanup"
	@echo "    logs                          - View logs from all services"
	@echo ""
	@echo "🐚 Shell Access:"
	@echo "    api-shell                     - Access Django API container shell"
	@echo "    ui-shell                      - Access React UI container shell"
	@echo "    db-shell                      - Access PostgreSQL database shell"
	@echo ""
	@echo "📦 UV Dependency Management:"
	@echo "    api-deps-add PKG=name         - Add new dependency (e.g., make deps-add PKG=requests)"
	@echo "    api-deps-add-dev PKG=name     - Add development dependency"
	@echo "    api-deps-remove PKG=name      - Remove dependency"
	@echo "    api-deps-sync                 - Sync dependencies (install/update from lock file)"
	@echo "    api-deps-update               - Update all dependencies to latest versions"
	@echo "    api-deps-rebuild              - Clean rebuild virtual environment"
	@echo "    api-deps-export               - Export requirements.txt for compatibility"
	@echo ""
	@echo "🗄️  Database Operations:"
	@echo "    api-migrations                - Create and apply database migrations"
	@echo "    api-migrations-check          - Check for unapplied migrations"
	@echo "    reset-db                      - Reset database (⚠️  destructive)"
	@echo "    load-fixtures                  - Load test data fixtures"
	@echo "    dump-fixtures                  - Export current data as fixtures"
	@echo "    create-cache-table            - Create Django cache table"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "    api-test                      - Run all tests with coverage"
	@echo "    api-test-fast                 - Run tests without coverage (faster)"
	@echo "    api-test-users                - Run user model tests only"
	@echo "    api-format                    - Format code with Ruff"
	@echo "    api-lint                      - Lint code and show issues"
	@echo "    api-type-check                - Run type checking with Pyright"
	@echo "    api-all-check                 - Run type checking, lint and format code"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "    clean                         - Clean up containers, volumes, and cache"
	@echo "    status                        - Show status of all services"

# ============================== Docker Compose Operations ==============================

# Setup all environment variables
env-setup:
	@echo "🔧 Setting environment variables..."
	@chmod +x scripts/setup_envs.sh
	@./scripts/setup_envs.sh

# Start all services in development mode
up:
	@echo "🚀 Starting Django + React development environment..."
	$(DC) up --watch $(SERVICES)

# Stop all services and cleanup
down:
	@echo "🛑 Stopping all services..."
	$(DC) down --remove-orphans
	@echo "✅ All services stopped"

# Build from scratch with fresh containers
build:
	@echo "🔨 Building Django + React from scratch..."
	@make env-setup
	$(DC) build --no-cache $(SERVICES)
	@echo "✅ All services built successfully"

# View logs from all services
logs:
	@echo "📋 Viewing logs from all services..."
	$(DC) logs -f

# Show status of all services
status:
	@echo "📊 Service Status:"
	$(DC) ps

# =================================== Shell Access =======================================
# Access Django API container shell
api-shell:
	@echo "🐚 Accessing Django API container shell..."
	$(EXEC) django_api bash

# Access React UI container shell
ui-shell:
	@echo "🐚 Accessing React UI container shell..."
	$(EXEC) react_ui bash

# Access PostgreSQL database shell
db-shell:
	@echo "🗄️  Accessing PostgreSQL database shell..."
	$(EXEC) database psql -U $${POSTGRES_USR} -d $${POSTGRES_DB}

# ============================== Command Execution Helpers ==============================
# Execute command in Django API container
exec-api:
	$(EXEC) django_api $(CMD)

# Execute command in React UI container
run-ui:
	$(EXEC) react_ui $(CMD)

# ============================== UV Dependency Management ==============================
# Add new production dependency
api-deps-add:
	@echo "📦 Adding dependency: $(PKG)"
	@make exec-api CMD="uv add $(PKG)"
	@make exec-deps-compile
	@make exec-deps-sync
	@echo "✅ Dependency $(PKG) added. Rebuilding container..."

# Add new development dependency
api-deps-add-dev:
	@echo "📦 Adding development dependency: $(PKG)"
	@make exec-api CMD="uv add --dev $(PKG)"
	@make exec-deps-compile
	@make exec-deps-sync
	@echo "✅ Development dependency $(PKG) added."
	

# Remove dependency
api-deps-remove:
	@echo "🗑️  Removing dependency: $(PKG)"
	@make exec-api CMD="uv remove $(PKG)"
	@make exec-deps-compile
	@make api-deps-sync
	@echo "✅ Dependency $(PKG) removed."

# Sync dependencies (install from lock file)
api-deps-sync:
	@echo "🔄 Syncing dependencies from lock file..."
	@make exec-api CMD="uv sync --extra dev"
	@echo "✅ Dependencies synchronized"

# Clean rebuild virtual environment
api-deps-rebuild:
	@echo "🔨 Rebuilding dependencies..."
	@make api-deps-compile
	@make api-deps-sync
	@echo "✅ Virtual environment rebuilt"

# Update uv.lock file with current dependencies from pyproject.toml
api-deps-compile:
	@echo "📄 Updating uv.lock "
	@make exec-api CMD="uv pip compile --extra dev pyproject.toml"
	@echo "✅ uv.lock successfully updated"

# ============================== Database Operations ==============================
# Create and apply database migrations
api-migrations:
	@echo "🗄️  Creating database migrations..."
	@make exec-api CMD="$(UV_MANAGE) makemigrations"
	@echo "🗄️  Applying database migrations..."
	@make exec-api CMD="$(UV_MANAGE) migrate"
	@echo "✅ Database migrations completed"

# Check for unapplied migrations
api-migrations-check:
	@echo "🔍 Checking for unapplied migrations..."
	@make exec-api CMD="$(UV_MANAGE) showmigrations --plan"

# Create Django cache table for database cache backend
api-create-cache-table:
	@echo "🗄️  Creating Django cache table..."
	@make exec-api CMD="$(UV_MANAGE) createcachetable"
	@echo "✅ Cache table created"

# ============================== Code Quality & Testing ==============================
api-all-check:
	@make api-format
	@make api-lint
	@make api-type-check

# Format code with Ruff
api-format:
	@echo "🎨 Formatting code with Ruff..."
	@make exec-api CMD="ruff format ."
	@echo "✅ Code formatting completed"

# Lint code and show issues
api-lint:
	@echo "🔍 Linting code with Ruff..."
	@make exec-api CMD="ruff check --fix ."
	@echo "✅ Code linting completed"

# Run type checking
api-type-check:
	@echo "🔍 Running type checking with Pyright..."
	@make exec-api CMD="pyright"
	@echo "✅ Type checking completed"

# ============================== Database Utilities ==============================
# Reset database (⚠️  DESTRUCTIVE - will delete all data)
api-reset-db:
	@echo "⚠️  Resetting database (this will delete all data)..."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "\n🗄️  Resetting database..."; \
		make exec-api CMD="$(UV_MANAGE) flush --noinput"; \
		make migrate; \
		make create-cache-table; \
		echo "✅ Database reset completed"; \
	else \
		echo "\n❌ Database reset cancelled"; \
	fi

# Export current data as fixtures
dump-fixtures:
	@echo "📤 Exporting database fixtures..."
	@make exec-api CMD="$(UV_MANAGE) dumpdata auth --natural-primary --natural-foreign --indent 2 > fixtures/auth.json"
	@make exec-api CMD="$(UV_MANAGE) dumpdata users --natural-primary --natural-foreign --indent 2 > fixtures/users.json"
	@echo "✅ Fixtures exported to fixtures/ directory"

# Load test data fixtures
load-fixtures:
	@echo "📥 Loading database fixtures..."
	@make exec-api CMD="$(UV_MANAGE) loaddata fixtures/auth.json"
	@make exec-api CMD="$(UV_MANAGE) loaddata fixtures/users.json"
	@echo "✅ Fixtures loaded successfully"

# ============================== Testing ==============================
# Run all tests with coverage report
api-test:
	@echo "🧪 Running all tests with coverage..."
	@make exec-api CMD="$(PYTEST_COV) tests/"
	@echo "✅ All tests completed. Coverage report generated."

# Run tests without coverage (faster for development)
api-test-fast:
	@echo "🧪 Running tests (fast mode)..."
	@make exec-api CMD="$(PYTEST_FAST) tests/"
	@echo "✅ Fast tests completed"

# Run specific test suites
api-test-users:
	@echo "🧪 Running user model tests..."
	@make exec-api CMD="$(PYTEST_FAST) tests/test_users_models.py"

api-test-celery:
	@echo "🧪 Running Celery task tests..."
	@make exec-api CMD="$(PYTEST_FAST) tests/test_celery_tasks.py"

# ============================== Cleanup & Utilities ===============================
# Clean up containers, volumes, and cache
clean:
	@echo "🧹 Cleaning up Docker resources..."
	$(DC) down --volumes --remove-orphans
	docker system prune -a --volumes -f 
	@echo "✅ Cleanup completed"

# Show comprehensive project status
project-status:
	@echo "📊 Django + React PoC Status:"
	@echo ""
	@echo "🐳 Docker Services:"
	$(DC) ps
	@echo ""
	@echo "📦 Python Dependencies:"
	@make exec-api CMD="uv tree --depth 1"
	@echo ""
	@echo "🗄️  Database Status:"
	@make exec-api CMD="$(UV_MANAGE) showmigrations --plan | tail -5"

.PHONY: help up down build logs status api-shell ui-shell db-shell exec-api run-ui \
        api-deps-add api-deps-add-dev api-deps-remove api-deps-sync api-deps-update \
		api-deps-rebuild api-deps-export api-migrations api-migrations-check \
		api-create-cache-table api-format api-lint api-type-check reset-db dump-fixtures \
		load-fixtures api-test api-test-fast api-test-users api-test-celery \
    	clean project-status