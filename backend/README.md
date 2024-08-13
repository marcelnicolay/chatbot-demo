# Chatdemo API

## Running local using docker (recommended)
```bash
docker compose build
docker compose up
```

Open https://localhost:8000/docs and try out using openapi documentation

## Routes
POST /api/threads/
POST /api/threads/{thread_id}/chat/

# Contributing

## Create Virtual Env

```bash
python3 -m venv .venv
.venv/bin/pip install -U pip setuptools
.venv/bin/pip install poetry
```

## Installing dependencies

```bash
poetry install
```

## Running tests with pytest
```bash
pytest
```

## type checking and lint
This codebase is uses mypy for type checking and ruff for everything else

To run type checker

```bash
mypy src
```

To run the linter and code formater checker

```bash
ruff check src
ruff format src
```

## Running fastapi server using uvicorn local
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

