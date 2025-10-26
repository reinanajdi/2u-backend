from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.security import hash_password

def create_user(db: Session, *, full_name, email, password, phone=None, role=UserRole.client, lat=None, lon=None):
    u = User(full_name=full_name, email=email, password_hash=hash_password(password),
             phone=phone, role=role, latitude=lat, longitude=lon)
    db.add(u); db.commit(); db.refresh(u)
    return u

def get_user_by_email(db: Session, email: str): 
    return db.query(User).filter(User.email == email).first()
