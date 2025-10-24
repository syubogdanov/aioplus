PYTHON = python -m


# Formatters
format: black

black:
	$(PYTHON) black aioplus/ tests/


# Linters
lint: ruff mypy

mypy:
	$(PYTHON) mypy aioplus/

ruff:
	$(PYTHON) ruff check aioplus/ tests/


# Tests
test: unit-tests

unit-tests:
	$(PYTHON) pytest tests/
