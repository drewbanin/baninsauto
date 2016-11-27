
build:
	rm -rf dist
	mkdir dist
	python build.py

deploy: build
	surge dist baninsauto.com
