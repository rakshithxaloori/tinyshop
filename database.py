import os
from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = os.environ["DB_URL"]
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
