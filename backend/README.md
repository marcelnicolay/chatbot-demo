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

## Running fastapi server using uvicorn local
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Running fastapi server using gunicorn local
```bash
gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker --bind :8000
```
