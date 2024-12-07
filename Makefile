.PHONY: test cov lint doc

TEST ?= .
TEST_PATH = tests/
SRC_PATH = src/
PACKAGE_PATH= src/tonie_sync/
COV_PATH = htmlcov/
DOC_PATH = docs/Reference
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

help:
	@echo "------------------ HELP ------------------------------"
	@echo "To execute a target, use 'make [target]'."
	@echo "------------------------------------------------------"
	@echo "Available targets:"
	@echo "cov        - Run tests and print coverage."
	@echo "test       - Run tests."
	@echo "lint       - Run linting with pre-commit on all files."
	@echo "doc        - Use pydocs-markdown to create docs."
	@echo "------------------------------------------------------"

test:
ifeq ($(ARGS),)
	python -m pytest
else
	python -m pytest ./test/$(ARGS)
endif

cov:
	python -m pytest --cov=$(SRC_PATH) --cov-report term-missing $(TEST_PATH)

pre-commit:
	pre-commit run --all-files

lint: mypy pre-commit

doc:
	mkdocs serve

mypy:
	mypy ./src --pretty
