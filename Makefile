VENV = poetry run

LIBRARY = aioplus
TESTS = tests


# Formatters
format: black

black:
	$(VENV) black ./$(LIBRARY)/ ./$(TESTS)/


# Linters
lint: ruff mypy

mypy:
	$(VENV) mypy ./$(LIBRARY)/

ruff:
	$(VENV) ruff check ./$(LIBRARY)/ ./$(TESTS)/


# Tests
test: unit-tests

unit-tests:
	$(VENV) pytest ./$(TESTS)/
