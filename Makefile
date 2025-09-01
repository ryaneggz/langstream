.PHONY: start lint format

start:
	python -m src.langstream

dev:
	uv run uvicorn src.langstream.__main__:app --reload

format:
	uvx ruff format