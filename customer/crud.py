from sqlalchemy.orm import Session

from customer import model


def get_customers(db: Session, skip: str = None, limit: int = 50):
    print(db.query(model.Customer).first())
    return []
