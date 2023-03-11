#!/bin/sh
set -e

if [ "$1" = 'gunicorn' ]; then
    exec "$@" -b 127.0.0.1:8000 userman2.wsgi
fi

exec "$@"
