from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "task_queue",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

celery.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)