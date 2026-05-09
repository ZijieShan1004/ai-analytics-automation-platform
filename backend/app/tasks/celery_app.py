from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "analytics_platform_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.analytics_tasks", "app.tasks.cleanup_tasks"],
)

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.timezone = "UTC"
celery_app.conf.enable_utc = True