import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.base import Base

class Role(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(Enum(Role), default=Role.viewer, nullable=False)
    is_active = Column(Boolean, default=True)
