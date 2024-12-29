PY := python3
VENV_NAME = venv

.PHONY: all

all:
	echo all

env:
	$(PY) -m venv $(VENV_NAME)
	source ./$(VENV_NAME)/bin/activate # permission denied ???
	pip install -r requirements-dev.txt
