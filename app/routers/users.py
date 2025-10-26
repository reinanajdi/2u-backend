from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserOut
from app.deps import get_current_user
from app.utils.geo import haversine_km

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return current

@router.get("/nearby", response_model=List[UserOut])
def nearby_providers(lat: float, lon: float, radius_km: float = 10, db: Session = Depends(get_db)):
    providers = db.query(User).filter(User.role == UserRole.provider, User.is_available == True).all()
    return [p for p in providers if p.latitude and haversine_km(lat, lon, p.latitude, p.longitude) <= radius_km]
