import os
from celery import Celery

REDIS_URL = os.environ["REDIS_URL"]

# Define the Celery app
celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Optional configuration, see Celery documentation for more details
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    enable_utc=True,
)

from app.checkout import tasks
import app.main
