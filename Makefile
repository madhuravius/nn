SHELL := bash
PYTHON_VENV = source .venv/bin/activate &&

.venv:
	python -m venv .venv
.PHONY: .venv

install: .venv
	$(PYTHON_VENV) pip install \
		-e .[test]
.PHONY: install

build: install .venv
	python -m build --wheel
.PHONY: build

black:
	$(PYTHON_VENV) black ./nn
.PHONY: black

isort:
	$(PYTHON_VENV) isort ./nn
.PHONY: isort

pretty: black isort
.PHONY: pretty

black_check:
	$(PYTHON_VENV) black ./nn --check
.PHONY: black_check

isort_check:
	$(PYTHON_VENV) isort --check-only ./nn
.PHONY: isort_check

mypy_check:
	$(PYTHON_VENV) mypy ./nn
.PHONY: mypy_check

lint: black_check isort_check mypy_check
.PHONY: lint

test:
	$(PYTHON_VENV) pytest tests -v --cov=./nn --cov-report term-missing
.PHONY: test

run: .venv
	$(PYTHON_VENV) ./run.sh
.PHONY: run

pex: .venv
	$(PYTHON_VENV) pex . \
		--python-shebang="#!/usr/bin/env python3" \
		--console-script nn -v -o nn.pex \
		--disable-cache
	chmod +x ./nn.pex
.PHONY: pex

pex_debug: pex
	rm -Rf temp || true
	mkdir temp
	cp nn.pex temp/nn.pex
	cd temp && unzip nn.pex
.PHONY: pex_debug

clean:
	rm -Rf temp || true
	rm -Rf dist || true
	rm -Rf .venv || true
.PHONY: clean
