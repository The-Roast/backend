from celery.app import Celery
from celery.utils.log import get_task_logger

from theroast.config import server_config

celery_app = Celery(
    __name__, broker=server_config.CELERY_BROKER_URL, backend=server_config.CELERY_BACKEND_URL
)
celery_app.conf.update(imports=["theroast.celery.tasks.email"])
logger = get_task_logger(__name__)