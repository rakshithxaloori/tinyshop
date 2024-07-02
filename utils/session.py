from typing import Any
from sqlmodel import Session
from database import engine


def get_session() -> Session:
    with Session(engine) as session:
        yield session


def update_refresh(
    db: Session,
    update_data: dict[str, Any],
    instance: Any,
):
    for key, value in update_data.item():
        setattr(instance, key, value)

    db.add(instance)
    db.commit()
    db.refresh(instance)
