# Wallet Service API

Это веб-приложение на FastAPI для управления балансом кошельков с использованием PostgreSQL.  

## Запуск приложения

### 1. Склонируйте репозиторий

```bash
git clone https://github.com/Frozet/wallet-service.git
cd wallet-service
```

### 2. Создайте .env файл

Создайте файл .env в корне проекта со следующим содержимым:
```bash
DATABASE_URL=postgresql://user:password@db:5432/wallet_db
```

### 3. Запустите контейнеры
```bash
docker-compose up --build
```

### 4. Создайте первую миграцию
```bash
docker exec -it <название контейнера fastapi_wallets> bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Выполнение тестов
```bash
docker-compose run app /start.sh test
```