#!/bin/bash
# Django Development Server Entrypoint
# Handles migrations, and starts development server
set -e pipefail

# =============================== Worker configuration ================================
# Calculate GUNICORN_WORKERS based on available CPUs if not already set:
# Formula: (2 × CPUs) + 1 — standard Gunicorn recommendation for optimal concurrency
# Ref: https://docs.gunicorn.org/en/stable/design.html#how-many-workers
if [ -z "$GUNICORN_WORKERS" ]; then
  MAX_WORKERS=4
  CPU_COUNT=$(nproc)

  BASE_WORKERS=$((CPU_COUNT < MAX_WORKERS ? CPU_COUNT : MAX_WORKERS))
  GUNICORN_WORKERS=$((BASE_WORKERS + 1))
fi

# Apply database migrations
echo "📦 Applying database migrations..."
python manage.py migrate --noinput

# Start development server
echo "🚀 Starting Django server on ${API_HOST}:${API_PORT} with ${GUNICORN_WORKERS} workers..."
echo "🐞 Debug mode: ON | ♻️ Auto-reload: ON"
exec python manage.py runserver ${API_HOST}:${API_PORT}