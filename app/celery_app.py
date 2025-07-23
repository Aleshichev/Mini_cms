# from celery import Celery

# celery_app = Celery(
#     "worker",
#     broker="redis://redis:6379/0",      # 🔁 Redis — как в docker-compose
#     backend="redis://redis:6379/1",     # 👈 можно использовать для хранения результата
#     include=["app.tasks.notify"],
# )

# celery_app.conf.update(
#     worker_hostname="worker123",
#     task_routes={
#         "app.tasks.*": {"queue": "main-queue"},
#     },
# )
