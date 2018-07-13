#!/bin/sh
set -e

if [ "$1" = 'gunicorn' ]; then
    export DATADOG_SERVICE_NAME=userman2
    exec ddtrace-run "$@" -b 127.0.0.1:8000 userman2.wsgi
fi

exec "$@"
