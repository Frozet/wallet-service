import uuid
import threading
from models.models import Wallet
from database import SessionLocal

# Тестовый ID кошелька
WALLET_ID = str(uuid.uuid4())

def create_wallet():
    db = SessionLocal()
    wallet = Wallet(id=WALLET_ID, balance=1000)
    db.add(wallet)
    db.commit()
    db.close()

def test_deposit_success(client):
    create_wallet()
    response = client.post(f"/api/v1/wallets/{WALLET_ID}/operation", json={
        "operation_type": "DEPOSIT",
        "amount": 500
    })
    assert response.status_code == 200
    assert response.json() == {"wallet_id": WALLET_ID, "new_balance": 1500}

def test_withdraw_success(client):
    create_wallet()
    response = client.post(f"/api/v1/wallets/{WALLET_ID}/operation", json={
        "operation_type": "WITHDRAW",
        "amount": 400
    })
    assert response.status_code == 200
    assert response.json() == {"wallet_id": WALLET_ID, "new_balance": 600}

def test_withdraw_insufficient_funds(client):
    create_wallet()
    response = client.post(f"/api/v1/wallets/{WALLET_ID}/operation", json={
        "operation_type": "WITHDRAW",
        "amount": 2000
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds"}

def test_get_balance(client):
    create_wallet()
    response = client.get(f"/api/v1/wallets/{WALLET_ID}")
    assert response.status_code == 200
    assert response.json() == {"wallet_id": WALLET_ID, "balance": 1000}

def modify_balance_concurrently(client, operation_type, amount, results):
    """Выполняет операцию (DEPOSIT или WITHDRAW) в параллельном потоке"""
    response = client.post(f"/api/v1/wallets/{WALLET_ID}/operation", json={
        "operation_type": operation_type,
        "amount": amount
    })
    results.append(response.json())

def test_concurrent_requests(client):
    create_wallet()

    threads = []
    results = []

    # Запускаем 5 потоков на пополнение и 5 на снятие средств
    for _ in range(5):
        t1 = threading.Thread(target=modify_balance_concurrently, args=(client, "DEPOSIT", 100, results))
        t2 = threading.Thread(target=modify_balance_concurrently, args=(client, "WITHDRAW", 50, results))
        threads.extend([t1, t2])

    # Запускаем все потоки
    for thread in threads:
        thread.start()

    # Дожидаемся завершения всех потоков
    for thread in threads:
        thread.join()

    # Проверяем итоговый баланс
    response = client.get(f"/api/v1/wallets/{WALLET_ID}")
    assert response.status_code == 200

    expected_balance = 1000 + 500 - 250
    assert response.json() == {"wallet_id": WALLET_ID, "balance": expected_balance}