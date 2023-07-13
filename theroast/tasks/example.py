from theroast.extensions import celery
import time

@celery.task
def send_email(newsletter):
    time.sleep(5)
    return "OK"