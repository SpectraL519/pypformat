.PHONY: tests clean_tests coverage clean_cov build clean_build ruff clean_ruff clean_all install upload

tests-simple:
	pytest test/

# tox will generate the coverage report
tests-tox:
	tox

clean-tests:
	rm -rf .pytest_cache/ .tox/

clean-cov:
	rm -rf .coverage*

build:
	python -m build

clean-build:
	rm -rf build/ dist/ *.egg-info README_pypi.md

ruff:
	ruff format && ruff check --fix

clean-ruff:
	rm -rf .ruff_cache/

clean-all: clean-tests clean-cov clean-build clean-ruff

install:
	pip uninstall -y pypformat || true
	$(MAKE) clean-build
	python -m build
	pip install .

upload: build
	python scripts/preprocess_md_doc.py
	python -m twine upload dist/*
