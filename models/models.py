from pydantic import BaseModel
from sqlalchemy import Column, Numeric
from pydantic import BaseModel
from enum import Enum as PyEnum
import uuid
from database import Base
from sqlalchemy.dialects.postgresql import UUID

class OperationType(PyEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric, default=0)

class Operation(BaseModel):
    operation_type: OperationType
    amount: float