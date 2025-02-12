# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# ENV DB_URL=$DB_URL
# ENV RAZORPAY_KEY_ID=$RAZORPAY_KEY_ID
# ENV RAZORPAY_KEY_SECRET=$RAZORPAY_KEY_SECRET
ARG DB_URL
ARG RAZORPAY_KEY_ID
ARG RAZORPAY_KEY_SECRET

ENV PYTHONPATH=.

# 
CMD ["fastapi", "run", "app.main.py", "--port", "80"]
