#!/bin/bash

# Ожидаем, пока база данных станет доступной
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done

# Применяем миграции с явным завершением при ошибке
echo "Applying migrations..."
if ! alembic upgrade head; then
  echo "❌ Migrations failed. Exiting..."
  exit 1
fi

# Если передали аргумент `test`, запускаем тесты
if [ "$1" == "test" ]; then
  echo "Running tests..."
  pytest --tb=short -v tests/
else
  echo "Starting application..."
  uvicorn main:app --host 0.0.0.0 --port 8000
fi