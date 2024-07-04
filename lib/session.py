from typing import Any
from sqlmodel import Session
from database import engine


def get_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def update_instance(
    db: Session,
    data: dict[str, Any],
    instance: Any,
):
    for key, value in data.items():
        setattr(instance, key, value)

    db.add(instance)
