PY := python3
PYM := $(PY) -m

COLOR_RESET  := \033[0m
COLOR_GREEN  := \033[1;32m
COLOR_CYAN := \033[1;33m
COLOR_CYAN   := \033[1;36m
COLOR_RED    := \033[1;31m

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
	@echo "$(COLOR_CYAN)> Creating virtual environment...$(COLOR_RESET)"; \
	$(PYM) venv venv && \
	echo "$(COLOR_CYAN)> Installing dev dependencies...$(COLOR_RESET)"; \
	. venv/bin/activate && pip install -r requirements-dev.txt > /dev/null

clean-venv:
	@echo "$(COLOR_CYAN)> Removing virtual environment...$(COLOR_RESET)"; \
	rm -rf venv/

tests-simple:
	@echo "$(COLOR_CYAN)> Running tests (simple) ...$(COLOR_RESET)"; \
	$(PYM) pytest test/

tests-tox:
	@echo "$(COLOR_CYAN)> Running tests (tox)...$(COLOR_RESET)"; \
	$(PYM) tox

clean-tests:
	@echo "$(COLOR_CYAN)> Cleaning test artifacts...$(COLOR_RESET)"; \
	rm -rf .pytest_cache/ .tox/

clean-cov:
	@echo "$(COLOR_CYAN)> Cleaning coverage files...$(COLOR_RESET)"; \
	rm -rf .coverage*

clean-build:
	@echo "$(COLOR_CYAN)> Cleaning build artifacts...$(COLOR_RESET)"; \
	rm -rf build/ dist/ *.egg-info README_pypi.md

build: clean-build
	@ALL_TAGS=$$(git tag | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$$' | sort -V); \
	LATEST_TAG=$$(echo "$$ALL_TAGS" | tail -n 1); \
	echo "$(COLOR_CYAN)> Latest git tag: $(COLOR_YELLOW)$$LATEST_TAG$(COLOR_RESET)"; \
	PY_VERSION=$$(sed -n 's/^version *= *"\([^"]*\)".*$$/\1/p' pyproject.toml); \
	echo "$(COLOR_CYAN)> Current version (pyproject.toml): $(COLOR_CYAN)$$PY_VERSION$(COLOR_RESET)"; \
	if [ "$${LATEST_TAG#v}" != "$$PY_VERSION" ]; then \
		echo "$(COLOR_RED)> ERROR: Git tag ($$LATEST_TAG) and pyproject version ($$PY_VERSION) do not match.$(COLOR_RESET)"; \
		exit 1; \
	fi; \
	echo "$(COLOR_CYAN)> Processing project README...$(COLOR_RESET)"; \
	$(PY) scripts/process_md_doc.py --version $$LATEST_TAG > /dev/null; \
	echo "$(COLOR_CYAN)> Building the distribution...$(COLOR_RESET)"; \
	$(PYM) build > /dev/null; \
	BUILD_EXIT_CODE=$$?; \
	if [ $$BUILD_EXIT_CODE -eq 0 ]; then \
		echo "$(COLOR_GREEN)> Build complete.$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_RED)> Build failed.$(COLOR_RESET)"; \
		exit $$BUILD_EXIT_CODE; \
	fi

ruff:
	@echo "$(COLOR_CYAN)> Running formatter...$(COLOR_RESET)"; \
	$(PYM) ruff format; \
	echo "$(COLOR_CYAN)> Running linter...$(COLOR_RESET)"; \
	$(PYM) ruff check --fix

clean-ruff:
	@echo "$(COLOR_CYAN)> Cleaning ruff cache...$(COLOR_RESET)"; \
	rm -rf .ruff_cache/

clean-all: clean-venv clean-tests clean-cov clean-build clean-ruff

install:
	@echo "$(COLOR_CYAN)> Reinstalling local package...$(COLOR_RESET)"; \
	$(PYM) pip uninstall -y pypformat > /dev/null || true; \
	$(PYM) pip install . > /dev/null

upload: clean-build build
	@echo "$(COLOR_CYAN)> Uploading distribution with twine...$(COLOR_RESET)"; \
	$(PYM) twine upload dist/*
