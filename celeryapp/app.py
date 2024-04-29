import logging

from celery import Celery
from celery.signals import worker_process_init

from backend.model import init_db
from backend.settings import settings


app = Celery(__name__, broker=settings.celery_broker_url)

app.autodiscover_tasks(["celeryapp.tasks"])
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@worker_process_init.connect
def init_worker(**kwargs):
    """Run in each worker process to initialize database connection"""
    init_db()
