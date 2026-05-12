# casework-task-api

REST API for managing caseworker tasks. Built with FastAPI and PostgreSQL.

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pytest

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy the example env file and update with your local database credentials:

```bash
cp .env.example .env
```

Start the server:

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Running tests

```bash
pytest
```