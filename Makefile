.PHONY: lint format

start:
	python -m src.main

dev:
	uv run uvicorn src.main:app --reload

format:
	uvx ruff format