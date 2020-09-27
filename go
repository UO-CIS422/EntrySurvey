#! /bin/sh
. env/bin/activate
port=4522
nohup gunicorn --bind="0.0.0.0:${port}" flask_poll:app &
echo "Poll starting, port ${port}"
