FROM python:3.10-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./app /app/app

COPY alembic.ini /app/
COPY alembic /app/alembic

# CMD ["uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "app.main:main_app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

