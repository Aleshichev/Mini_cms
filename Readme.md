#alembic revision --autogenerate -m "all tables"

#docker compose run --rm api taskiq worker app.taskiq_broker:broker --fs-discover --tasks-pattern "**/tasks"    # запустить worker в контейнере