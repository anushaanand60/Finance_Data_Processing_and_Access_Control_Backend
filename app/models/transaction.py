import enum
from sqlalchemy import Column, Integer, String, Numeric, Date, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import date
from app.db.base import Base

class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, index=True, nullable=False)
    date = Column(Date, default=date.today, nullable=False)
    notes = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_by = relationship("User")
