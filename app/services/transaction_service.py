from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import date
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.is_deleted == False).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 50, type_filter: Optional[TransactionType] = None, category_filter: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(Transaction).filter(Transaction.is_deleted == False)
    if type_filter:
        query = query.filter(Transaction.type == type_filter)
    if category_filter:
        query = query.filter(Transaction.category == category_filter)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    query = query.order_by(desc(Transaction.date), desc(Transaction.id))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def create_transaction(db: Session, transaction_in: TransactionCreate, user_id: int):
    create_data = transaction_in.model_dump(exclude_unset=True)
    # If date is passed as None or omitted, we remove it to let SQLAlchemy's default kick in
    '''
    So earlier here, I encountered a mismatch where the API schema allowed a nullable date field, but the database enforced it as non-nullable, 
    causing the transaction creation to fail which I have resolved now by using a default_factory in the Pydantic schema to automatically assign the current date. 
    This is now consistent with the database too.
    '''
    if create_data.get("date") is None:
        create_data.pop("date", None)
    db_transaction = Transaction(**create_data, created_by_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction