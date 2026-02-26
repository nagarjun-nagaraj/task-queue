import time
from app.celery_app import celery

@celery.task(bind=True)
def send_email(self, recipient: str, subject: str):
    time.sleep(3)  # simulate sending email
    return f"Email sent to {recipient} with subject: {subject}"

@celery.task(bind=True)
def process_data(self, data: dict):
    time.sleep(5)  # simulate heavy processing
    result = {key: str(value).upper() for key, value in data.items()}
    return f"Processed: {result}"