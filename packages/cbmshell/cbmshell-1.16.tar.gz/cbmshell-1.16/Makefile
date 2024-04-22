.PHONY: install
install:
	pip3 install . --upgrade

.PHONY: build
build:
	rm -rf dist
	python3 setup.py sdist bdist_wheel

.PHONY: upload
upload: build
	python3 -m twine upload dist/*

.PHONY: unittest
unittest:
	cd test ; cbm-shell --test *.transcript
	rm -rf test/output

.PHONY: lint
lint:
	flake8 cbm_shell test
