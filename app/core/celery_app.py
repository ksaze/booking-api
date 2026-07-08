from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "fitness_studio",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["core.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TIMEZONE,
    enable_utc=True,
    task_track_started=True,
)

# Run a worker with:
#   celery -A core.celery_app.celery_app worker --loglevel=info
