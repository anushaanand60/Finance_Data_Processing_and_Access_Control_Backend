from typing import Any, List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.services import transaction_service
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionList
from app.models.user import Role, User as UserModel
from app.models.transaction import TransactionType

router = APIRouter()

allow_analyst_admin = deps.RoleChecker([Role.analyst, Role.admin])
allow_admin = deps.RoleChecker([Role.admin])

@router.get("/", response_model=TransactionList)
def read_transactions(db: Session = Depends(deps.get_db), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), type: Optional[TransactionType] = None, category: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None, current_user: UserModel = Depends(allow_analyst_admin)) -> Any:
    return transaction_service.get_transactions(db, skip, limit, type, category, start_date, end_date)

@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(deps.get_db), current_user: UserModel = Depends(allow_analyst_admin)) -> Any:
    transaction = transaction_service.get_transaction(db, transaction_id=transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=Transaction)
def create_transaction(*, db: Session = Depends(deps.get_db), transaction_in: TransactionCreate, current_user: UserModel = Depends(allow_admin)) -> Any:
    return transaction_service.create_transaction(db=db, transaction_in=transaction_in, user_id=current_user.id)