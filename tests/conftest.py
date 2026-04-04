import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.api.deps import get_db
from app.db.base import Base
from app.models.user import User, Role
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_users(db):
    admin = User(email="admin@test.com", hashed_password=get_password_hash("pass"), role=Role.admin, full_name="Admin")
    analyst = User(email="analyst@test.com", hashed_password=get_password_hash("pass"), role=Role.analyst, full_name="Analyst")
    viewer = User(email="viewer@test.com", hashed_password=get_password_hash("pass"), role=Role.viewer, full_name="Viewer")
    db.add_all([admin, analyst, viewer])
    db.commit()
    db.refresh(admin)
    db.refresh(analyst)
    db.refresh(viewer)
    return {"admin": admin, "analyst": analyst, "viewer": viewer}

@pytest.fixture
def auth_headers(client, test_users):
    def get_token(role: str):
        response = client.post(f"/api/v1/auth/login", data={"username": f"{role}@test.com", "password": "pass"})
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return get_token
