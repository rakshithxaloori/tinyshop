# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code

ARG TEST_ENDPOINT

ENV PYTHONPATH=.

# 
CMD ["fastapi", "run", "main.py", "--port", "8081"]
