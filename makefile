
build:
	mkdir -p dist
	rm -rf dist/*
	python build.py

deploy: build
	surge dist baninsauto.com
