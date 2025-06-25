.PHONY: help clean install install-dev test test-all lint format type-check security build upload upload-test docs clean-build clean-pyc clean-test

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

install: clean ## install the package to the active Python's site-packages
	pip install .

install-dev: clean ## install the package and development dependencies
	pip install -e ".[dev,test,docs]"

install-hooks: ## install pre-commit hooks
	pre-commit install

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	pytest --cov=pyhetznerserver --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint: ## check style with flake8
	flake8 pyhetznerserver tests

format: ## format code with black and isort
	black pyhetznerserver tests
	isort pyhetznerserver tests

type-check: ## run type checking with mypy
	mypy pyhetznerserver --ignore-missing-imports

security: ## run security checks
	bandit -r pyhetznerserver/
	safety check

docs: ## generate Sphinx HTML documentation
	rm -f docs/pyhetznerserver.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pyhetznerserver
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@echo "Documentation generated in docs/_build/html/index.html"

build: clean ## builds source and wheel package
	python -m build
	ls -l dist

check-build: build ## check built package
	twine check dist/*

upload-test: build check-build ## upload package to Test PyPI
	twine upload --repository testpypi dist/*

upload: build check-build ## upload package to PyPI
	twine upload dist/*

dev-setup: install-dev install-hooks ## setup development environment
	@echo "Development environment setup complete!"

run-example: ## run the example usage script
	python -m pyhetznerserver.example_usage

test-dry-run: ## run tests in dry-run mode
	python -m pytest tests/test_basic.py -v

check-all: lint type-check security test ## run all checks

release-check: clean check-all build check-build ## run all checks before release
	@echo "All checks passed! Ready for release."

# Docker related commands (if needed in the future)
docker-build: ## build docker image
	docker build -t pyhetznerserver .

docker-run: ## run docker container
	docker run --rm -it pyhetznerserver

# Development utilities
bump-patch: ## bump patch version
	bump2version patch

bump-minor: ## bump minor version
	bump2version minor

bump-major: ## bump major version
	bump2version major

# GitHub utilities
create-release: ## create a new GitHub release (requires gh CLI)
	gh release create

open-repo: ## open GitHub repository in browser
	gh repo view --web 