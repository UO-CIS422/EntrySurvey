#! /bin/sh
. env/bin/activate
port=7592
nohup gunicorn --bind="0.0.0.0:${port}" flask_poll:app &
echo "Poll starting, port ${port}"
