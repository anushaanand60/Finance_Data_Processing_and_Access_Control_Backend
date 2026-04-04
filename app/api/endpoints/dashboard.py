from typing import Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.services import dashboard_service
from app.models.user import Role, User as UserModel

router = APIRouter()

allow_all_roles = deps.RoleChecker([Role.viewer, Role.analyst, Role.admin])

@router.get("/summary", response_model=dict)
def read_dashboard_summary(db: Session = Depends(deps.get_db), current_user: UserModel = Depends(allow_all_roles)) -> Any:
    return dashboard_service.get_dashboard_summary(db)


