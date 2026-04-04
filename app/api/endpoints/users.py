from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.services import user_service
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import Role, User as UserModel

router = APIRouter()
allow_admin = deps.RoleChecker([Role.admin])

@router.get("/", response_model=List[User])
def read_users(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: UserModel = Depends(allow_admin)) -> Any:
    return user_service.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=User)
def create_user(*,db: Session = Depends(deps.get_db), user_in: UserCreate, current_user: UserModel = Depends(allow_admin)) -> Any:
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.")
    return user_service.create_user(db=db, user_in=user_in)