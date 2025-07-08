from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",      # 🔁 Redis — как в docker-compose
    backend="redis://redis:6379/1",     # 👈 можно использовать для хранения результата
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "main-queue"},
}