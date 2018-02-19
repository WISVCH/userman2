#!/bin/sh
set -e

if [ "$1" = 'gunicorn' ]; then
    exec "$@" -b 0.0.0.0 userman2.wsgi
fi

exec "$@"
