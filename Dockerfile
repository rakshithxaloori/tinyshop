# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code/app

ARG DB_URL
ENV DB_URL=$DB_URL

# 
CMD ["fastapi", "run", "app/main.py", "--port", "80"]