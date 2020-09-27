# We use npm and webpack to compile index.js
# into dist/main.js with modules specified in
# package.json

default: modules dist/main.js

modules:
	npm install

dist/main.js: modules
	npm run build

clean:
	rm -rf node_modules

