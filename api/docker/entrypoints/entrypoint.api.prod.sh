#!/bin/bash
# Applies migrations and starts the Django server using Gunicorn.
set -e pipefail

# Apply database migrations
echo "📦 Applying database migrations..."
python manage.py migrate --noinput

# Start the Django server with Gunicorn
echo "🚀 Starting Django server on ${API_HOST}:${API_PORT} with ${GUNICORN_WORKERS} workers..."
python -m gunicorn config.wsgi:application \
  --bind "${API_HOST}:${API_PORT}" \
  --workers "${GUNICORN_WORKERS}" \
  --timeout 120 \
  --log-level "${LOG_LEVEL}" \
  --access-logfile '-' \
  --error-logfile '-'