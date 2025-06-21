FROM python:3.10-slim

# Установка Poetry (последняя версия)
RUN pip install --no-cache-dir poetry

WORKDIR /app

# Копируем только файлы с зависимостями сначала (для кэширования слоев)
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости через Poetry (без установки виртуального окружения)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код
COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
