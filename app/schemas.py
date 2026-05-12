from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from app.models import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    due_date: datetime

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return value.strip()

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_future(cls, value):
        if value < datetime.now(tz=value.tzinfo):
            raise ValueError("Due date must be in the future")
        return value


class TaskUpdateStatus(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: datetime
    created_at: datetime
    is_overdue: bool = False

    @classmethod
    def from_orm_with_overdue(cls, task):
        now = datetime.now(tz=task.due_date.tzinfo)
        data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "is_overdue": (
                task.status != TaskStatus.done
                and task.due_date < now
            )
        }
        return cls(**data)

    class Config:
        from_attributes = True