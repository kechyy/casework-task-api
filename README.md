# casework-task-api

Task management REST API for HMCTS caseworkers built with FastAPI and PostgreSQL.

## Stack

- Python 3.9 / FastAPI
- PostgreSQL
- SQLAlchemy
- Pytest
- Docker

## Running with Docker

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Then start the services:

```bash
docker-compose up --build
```

API runs on `http://localhost:8001`
API docs at `http://localhost:8001/docs`

## Running locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| POST | /tasks | Create a task |
| GET | /tasks/{id} | Get task by ID |
| PATCH | /tasks/{id}/status | Update task status |
| DELETE | /tasks/{id} | Delete a task |

## Future improvements

- Alembic migrations for schema version control
- User authentication
- Email notifications for overdue tasks
- Priority levels