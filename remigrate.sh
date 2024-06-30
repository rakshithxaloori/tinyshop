rm sql_app.db
rm -rf alembic/versions/*
export DB_URL="sqlite:///./sql_app.db"
alembic revision --autogenerate
alembic upgrade head
# PYTHONPATH=. fastapi dev main.py
PYTHONPATH=. python3 local/local_foundation.py
PYTHONPATH=. python3 local/local_customer.py
