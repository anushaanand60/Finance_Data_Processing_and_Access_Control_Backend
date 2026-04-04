import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User, Role
from app.core.security import get_password_hash

def seed_admin_user():
    db: Session = SessionLocal()
    try:
        email = "admin@example.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("Creating initial admin user...")
            password = os.getenv("ADMIN_PASSWORD", "admin123")
            admin_user = User(email=email, hashed_password=get_password_hash(password), full_name="System Admin", role=Role.admin, is_active=True)
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
        else:
            print(f"User {email} already exists. Skipping seed.")
    except Exception as e:
        print(f"Error seeding user: {e}")
        db.rollback()
    finally:
        db.close()
        print("Seeding completed.")

if __name__ == "__main__":
    seed_admin_user()
