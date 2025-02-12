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
ARG TEST_DASHBOARD_SECRET
ARG LIVE_DASHBOARD_SECRET

ENV TEST_ENDPOINT=$TEST_ENDPOINT
ENV TEST_DASHBOARD_SECRET=$TEST_DASHBOARD_SECRET
ENV LIVE_DASHBOARD_SECRET=$LIVE_DASHBOARD_SECRET
ENV PYTHONPATH=.

# 
CMD ["fastapi", "run", "main.py", "--port", "80"]
