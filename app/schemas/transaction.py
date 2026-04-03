from typing import Optional
from datetime import date as dt_date
from pydantic import BaseModel, Field
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: TransactionType
    category: str
    date: dt_date = Field(default_factory=dt_date.today)
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    date: Optional[dt_date] = None
    notes: Optional[str] = None

class TransactionInDBBase(TransactionBase):
    id: int
    is_deleted: bool
    created_by_id: Optional[int] = None

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass

class TransactionList(BaseModel):
    items: list[Transaction]
    total: int
