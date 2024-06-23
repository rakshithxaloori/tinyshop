from sqlalchemy.orm import Session

from . import models, schemas


def get_customers(db: Session, skip: str = None, limit: int = 50):
    return db.query(schemas.Customer).order_by()
