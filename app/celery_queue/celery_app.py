from celery import Celery

from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.broker_url,
    backend=settings.result_backend_url,
)

celery_app.conf.task_routes = {
    "app.celery_queue.tasks.*": {"queue": "default"},
}
