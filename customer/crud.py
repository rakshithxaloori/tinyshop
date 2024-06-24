from sqlalchemy.orm import Session

from customer import models


def get_customers(db: Session, skip: str = None, limit: int = 50):
    print(db.query(models.Customer).first())
    return []
