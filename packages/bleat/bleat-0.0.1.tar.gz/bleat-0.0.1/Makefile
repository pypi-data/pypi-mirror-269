MAKEFLAGS += --warn-undefined-variables
SHELL = /bin/bash -o pipefail
.DEFAULT_GOAL := help
.PHONY: help install check lint pyright test install-hooks hooks docs dist publish

## display help message
help:
	@awk '/^##.*$$/,/^[~\/\.0-9a-zA-Z_-]+:/' $(MAKEFILE_LIST) | awk '!(NR%2){print $$0p}{p=$$0}' | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

venv = .venv
pip := $(venv)/bin/pip

$(pip):
# create venv using system python even when another venv is active
	PATH=$${PATH#$${VIRTUAL_ENV}/bin:} python3 -m venv --clear $(venv)
	$(venv)/bin/python --version
	$(pip) install pip~=24.0

$(venv): $(if $(value CI),|,) pyproject.toml $(pip)
	$(pip) install -e '.[dev]'
	touch $(venv)

# delete the venv
clean:
	rm -rf $(venv)

## create venv and install this package and hooks
install: $(venv) node_modules $(if $(value CI),,install-hooks)

## lint, format and type check
check: export SKIP=test
check: hooks

## lint and format
lint: export SKIP=pyright,test
lint: hooks

node_modules: package.json
	npm install --no-save
	touch node_modules

## run tests
test: $(venv)
	$(venv)/bin/pytest

## build distribution
dist: $(venv)
	# start with a clean slate (see setuptools/#2347)
	rm -rf src/*.egg-info
	# remove previous builds
	rm -rf dist/* build/*
	$(venv)/bin/python -m build --sdist --wheel

## publish to pypi
publish: $(venv)
	$(venv)/bin/twine upload dist/*

## list outdated packages
outdated: $(venv)
	$(venv)/bin/pip list --outdated
	npm outdated

## run pre-commit git hooks on all files
hooks: node_modules $(venv)
	$(venv)/bin/pre-commit run --show-diff-on-failure --color=always --all-files --hook-stage push

install-hooks: .git/hooks/pre-commit .git/hooks/pre-push
	$(venv)/bin/pre-commit install-hooks

.git/hooks/pre-commit: $(venv)
	$(venv)/bin/pre-commit install -t pre-commit

.git/hooks/pre-push: $(venv)
	$(venv)/bin/pre-commit install -t pre-push
