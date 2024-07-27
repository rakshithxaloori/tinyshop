from typing import Any
from fastapi import Request
from sqlmodel import Session


def get_session(request: Request):
    return request.state.db


def update_instance(
    db: Session,
    data: dict[str, Any],
    instance: Any,
):
    for key, value in data.items():
        setattr(instance, key, value)

    db.add(instance)
