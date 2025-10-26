from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.deps import get_current_user
from app.schemas import SRCreate, SROut
from app.models import RequestStatus, UserRole
from app.crud import requests as sr_crud

router = APIRouter(prefix="/requests", tags=["Service Requests"])

@router.post("/", response_model=SROut, status_code=201)
def create_request(payload: SRCreate, db: Session = Depends(get_db), me=Depends(get_current_user)):
    return sr_crud.create_request(db, client_id=me.id, description=payload.description, lat=payload.latitude, lon=payload.longitude)

@router.get("/", response_model=List[SROut])
def list_my_requests(limit: int = 50, offset: int = 0, db: Session = Depends(get_db), me=Depends(get_current_user)):
    if me.role == UserRole.client:
        return sr_crud.list_for_user(db, client_id=me.id, limit=limit, offset=offset)
    else:
        return sr_crud.list_for_user(db, provider_id=me.id, limit=limit, offset=offset)

@router.post("/{sr_id}/accept", response_model=SROut)
def accept_request(sr_id: int, db: Session = Depends(get_db), me=Depends(get_current_user)):
    if me.role != UserRole.provider:
        raise HTTPException(status_code=403, detail="Only providers can accept.")
    sr = sr_crud.assign_provider(db, sr_id=sr_id, provider_id=me.id)
    if not sr: raise HTTPException(status_code=404, detail="Request not found.")
    return sr

@router.post("/{sr_id}/status", response_model=SROut)
def update_status(sr_id: int, status: RequestStatus, db: Session = Depends(get_db), me=Depends(get_current_user)):
    sr = sr_crud.get_by_id(db, sr_id)
    if not sr: raise HTTPException(status_code=404, detail="Request not found.")
    if me.id not in {sr.client_id, sr.provider_id}:
        raise HTTPException(status_code=403, detail="Not allowed.")
    return sr_crud.update_status(db, sr_id=sr_id, status=status)
