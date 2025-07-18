#!/bin/bash
# Celery Worker Entrypoint
set -e pipefail

echo "🚀 Starting Celery with ${CELERY_WORKER_CONCURRENCY} workers..."
# Start the Celery worker process using the specified app
exec python -m celery -A config worker \
    # Set the logging level (e.g., info, debug, warning)
    --loglevel="${LOGLEVEL}" \
    # Define the number of concurrent worker processes
    --concurrency="${CELERY_WORKER_CONCURRENCY}" \

    