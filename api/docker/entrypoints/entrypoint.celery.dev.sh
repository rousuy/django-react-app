#!/bin/bash
# Celery Worker Entrypoint ready for production
set -e pipefail

# ================================== Worker configuration =========================================
# Calculate CELERY_WORKER_CONCURRENCY based on available CPUs if not already set.
# Formula: (2 × CPUs) + 1 — borrowed from Gunicorn's recommendation for handling I/O-bound workloads.
if [ -z "$CELERY_WORKER_CONCURRENCY" ]; then
  MAX_CELERY_WORKERS=4
  CPU_COUNT=$(nproc)

  BASE_WORKERS=$((CPU_COUNT < MAX_CELERY_WORKERS ? CPU_COUNT : MAX_CELERY_WORKERS))
  CELERY_WORKER_CONCURRENCY=$((BASE_WORKERS + 1))
fi

# Start the Celery worker process using the specified app
echo "🚀 Starting Celery with ${CELERY_WORKER_CONCURRENCY} workers..."
exec python -m celery -A config worker \
    # Set the logging level (e.g., info, debug, warning)
    --loglevel=${LOGLEVEL} \
    # Define the number of concurrent worker processes
    --concurrency="${CELERY_WORKER_CONCURRENCY}" \
    # Enable autoreload in development (restarts worker on code changes)
    --autoreload \
    # Disable gossip protocol (used for worker internals, not needed in most setups)
    --without-gossip \
    # Disable mingle (skips state syncing with other workers on startup)
    --without-mingle \
    # Disable heartbeat (avoids sending heartbeats to the broker; useful in dev or custom infra)
    --without-heartbeats
    