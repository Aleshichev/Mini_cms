FROM python:3.10-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./app /app/app

CMD ["uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
