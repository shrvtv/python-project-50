lint:
	uv run ruff check

test:
	uv run pytest

check: lint test

test-and-coverage-xml:
	uv run pytest --cov --cov-report=xml
