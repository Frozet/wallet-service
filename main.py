from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from models.models import OperationType, Wallet, Operation
from database import get_db

app = FastAPI()

@app.post("/api/v1/wallets/{wallet_id}/operation")
def modify_balance(wallet_id: uuid.UUID, operation: Operation, db: Session = Depends(get_db)):
    with db.begin():
        wallet = db.query(Wallet).with_for_update().filter(Wallet.id == wallet_id).first()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if operation.operation_type == OperationType.DEPOSIT:
            wallet.balance = float(wallet.balance) + operation.amount
        elif operation.operation_type == OperationType.WITHDRAW:
            if wallet.balance < operation.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            wallet.balance = float(wallet.balance) - operation.amount
        db.commit()
    return {"wallet_id": str(wallet_id), "new_balance": wallet.balance}

@app.get("/api/v1/wallets/{wallet_id}")
def get_balance(wallet_id: uuid.UUID, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"wallet_id": str(wallet_id), "balance": wallet.balance}
