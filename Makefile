# Construct Python Flask app with Javascript modules

default: rebuild

install: rebuild

rebuild: env js

run:
	(source env/bin/activate; gunicorn flask_poll:app)

env:    requirements.txt
	python3 -mvenv env
	pip3 install -r requirements.txt

js:
	(cd static/js; make)

clean:
	(cd static/js; make clean)
	rm -rf env

