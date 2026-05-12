import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Separate test database so we never touch the real one
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Replace real database with test database
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Wipe everything after each test — clean slate
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── Helpers ──────────────────────────────────────────

def create_sample_task(title="Review case documents", due_date="2027-01-01T09:00:00+00:00"):
    return client.post("/tasks/", json={
        "title": title,
        "description": "Sample description",
        "status": "todo",
        "due_date": due_date
    })


# ── Create ───────────────────────────────────────────

def test_create_task_succeeds():
    response = create_sample_task()
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Review case documents"
    assert data["status"] == "todo"
    assert data["is_overdue"] is False


def test_create_task_rejects_empty_title():
    response = client.post("/tasks/", json={
        "title": "   ",
        "due_date": "2027-01-01T09:00:00+00:00"
    })
    assert response.status_code == 422


def test_create_task_rejects_past_due_date():
    response = client.post("/tasks/", json={
        "title": "Valid title",
        "due_date": "2020-01-01T09:00:00+00:00"
    })
    assert response.status_code == 422


# ── Read ─────────────────────────────────────────────

def test_get_all_tasks_returns_list():
    create_sample_task("Task one")
    create_sample_task("Task two")
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id():
    created = create_sample_task()
    task_id = created.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_returns_404_when_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404


# ── Update ───────────────────────────────────────────

def test_update_task_status():
    created = create_sample_task()
    task_id = created.json()["id"]
    response = client.patch(f"/tasks/{task_id}/status", json={
        "status": "in_progress"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_update_status_returns_404_when_not_found():
    response = client.patch("/tasks/999/status", json={
        "status": "done"
    })
    assert response.status_code == 404


# ── Delete ───────────────────────────────────────────

def test_delete_task():
    created = create_sample_task()
    task_id = created.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    # Confirm it's actually gone
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_returns_404_when_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404