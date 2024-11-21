#!/usr/bin/env bash

set -e

export WORKER_CLASS="uvicorn.workers.UvicornWorker"
export GUNICORN_CONF="deploy/node_server/gunicorn.conf.py"
export APP_MODULE="main:app"

# Migrations
python -m alembic upgrade head

# Start Uvicorn with live reload
gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
