lint:
	uv run ruff check

test:
	uv run pytest

check: lint test
