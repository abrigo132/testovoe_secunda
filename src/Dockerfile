FROM python:3.12-slim

WORKDIR /src

# Устанавливаем зависимости для PostgreSQL клиента
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей (Alembic должен быть в pyproject.toml)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копирование исходного кода и entrypoint
COPY . .
RUN chmod +x entrypoint.sh  # Делаем entrypoint исполняемым внутри контейнера

# Используем entrypoint для инициализации перед запуском
ENTRYPOINT ["./entrypoint.sh"]