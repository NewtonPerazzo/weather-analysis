from celery import Celery
from config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "weather_analysis",
    broker=settings.rabbitmq_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.report_tasks",
    ],
)