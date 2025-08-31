.PHONY: lint format

start:
	python -m src.main

format:
	uvx ruff format