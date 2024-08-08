from typing import Any
from fastapi import Request
from sqlmodel import Session
from contextlib import contextmanager


from app.database import engine


@contextmanager
def create_task_session() -> Session:
    """Create a session that a task can use."""
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()


def get_session(request: Request) -> Session:
    return request.state.db


def update_instance(
    db: Session,
    data: dict[str, Any],
    instance: Any,
):
    for key, value in data.items():
        setattr(instance, key, value)

    db.add(instance)
