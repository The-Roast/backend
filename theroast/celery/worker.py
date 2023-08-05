from celery.app import Celery
from theroast.config import server_config

celery_app = Celery(
    __name__, broker=server_config.CELERY_BROKER_URL, backend=server_config.CELERY_BACKEND_URL
)

