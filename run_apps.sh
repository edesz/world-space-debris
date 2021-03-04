#!/bin/bash


HOST=localhost
PORT=8000
APP=${1:-flask}

if [[ "$APP" == 'bokeh' ]]; then
    cd bokeh-server-apps
    BK_APPS=$(ls bkapps/*.py)
    bokeh serve \
        --address="localhost" \
        --port=5006 \
        --allow-websocket-origin=${HOST}:${PORT} \
        ${BK_APPS}
else
    cd owd-flask-app
    gunicorn -w 1 --bind ${HOST}:${PORT} main:app
fi
