
build:
	python build.py

deploy: build
	surge dist
