.PHONY: start lint format

start:
	python -m src.langstream

dev:
	uv run uvicorn src.langstream.__main__:app --reload

format:
	uvx ruff format

build:
	docker build --push -t ghcr.io/ryaneggz/langstream:latest .

run:
	docker run \
	--rm \
	--name langstream \
	-p 8000:8000 \
	--env-file .env \
	ghcr.io/ryaneggz/langstream:latest