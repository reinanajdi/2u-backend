from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Login, Token, UserCreate, UserOut
from app.database import get_db
from app.crud.users import create_user, get_user_by_email
from app.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered.")
    user = create_user(db,
        full_name=payload.full_name, email=payload.email, password=payload.password,
        phone=payload.phone, role=payload.role, lat=payload.latitude, lon=payload.longitude)
    return user

@router.post("/login", response_model=Token)
def login(payload: Login, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
