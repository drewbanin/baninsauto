
build:
	mkdir -p dist
	rm -rf dist/*
	cp sitemap.xml robots.txt google8e8e114f5e8ab57d.html dist/
	python build.py

deploy: build
	surge dist baninsauto.com
