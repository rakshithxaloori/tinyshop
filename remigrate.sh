rm sql_app.db
rm alembic/versions/*
export DB_URL="sqlite:///./sql_app.db"
alembic revision --autogenerate
alembic upgrade head
PYTHONPATH=. fastapi dev main.py
