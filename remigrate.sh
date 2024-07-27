rm sql_app.db
rm -rf alembic/versions/*
export DB_URL="postgresql://postgres:postgres@localhost:5432/tinyshop"
echo $DB_URL
psql "postgresql://postgres:postgres@localhost:5432" -c "drop database tinyshop WITH (FORCE);"
psql "postgresql://postgres:postgres@localhost:5432" -c "create database tinyshop owner postgres;"
alembic revision --autogenerate
alembic upgrade head
PYTHONPATH=. python3 local/local_foundation.py
PYTHONPATH=. python3 local/local_customer.py
