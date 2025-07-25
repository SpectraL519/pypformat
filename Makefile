PY := python3
PYM := $(PY) -m

.PHONY: \
	prepare-venv \
	clean-venv \
	tests-simple \
	tests-tox \
	clean-tests \
	clean-cov \
	build \
	clean-build \
	ruff \
	clean-ruff \
	clean-all \
	install \
	upload

prepare-venv:
	$(PYM) venv venv && \
	. venv/bin/activate && \
	pip install -r requirements-dev.txt

clean-venv:
	rm -rf venv/

source-venv:
	. venv/bin/activate

tests-simple:
	$(PYM) pytest test/

# tox will generate the coverage report
tests-tox:
	$(PYM) tox

clean-tests:
	rm -rf .pytest_cache/ .tox/

clean-cov:
	rm -rf .coverage*

build:
	$(PYM) build
	$(PY) scripts/preprocess_md_doc.py

clean-build:
	rm -rf build/ dist/ *.egg-info README_pypi.md

ruff:
	$(PYM) ruff format && ruff check --fix

clean-ruff:
	rm -rf .ruff_cache/

clean-all: clean-venv clean-tests clean-cov clean-build clean-ruff

install:
	$(PYM) pip uninstall -y pypformat || true
	$(PYM) pip install .

upload: build
	$(PYM) twine upload dist/*
