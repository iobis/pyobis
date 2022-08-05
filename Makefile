all: build install

.PHONY: build install test docs distclean dist upload

build:
	python setup.py build

install:
	python -m pip install -e .

test:
	nosetests -v --with-coverage --cover-package=pyobis

test3:
	python3 -m "nose" -v --with-coverage --cover-package=pyobis

docs:
	cd docs;\
	make html

distclean:
	rm dist/*

dist:
	python setup.py sdist bdist_wheel --universal

register:
	python setup.py register

upload:
	twine upload dist/*
