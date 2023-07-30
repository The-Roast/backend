#! /usr/bin/env sh
set -e

echo "SET -E"

if [ -f /theroast/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
    echo "DEFAULT MOD1"
elif [ -f /theroast/main.py ]; then
    DEFAULT_MODULE_NAME=main
    echo "DEFAULT MOD2"
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

echo "SET APP_MODULE"

HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8888}
LOG_LEVEL=${LOG_LEVEL:-info}

echo "SET HOST"

# Start Uvicorn with live reload
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"