from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.deps import get_current_user
from app.schemas import MsgCreate, MsgOut
from app.crud.messages import create_message, list_messages
from app.crud.requests import get_by_id as get_sr

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/{request_id}", response_model=MsgOut, status_code=201)
def send_message(request_id: int, payload: MsgCreate, db: Session = Depends(get_db), me=Depends(get_current_user)):
    sr = get_sr(db, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found.")
    if me.id not in {sr.client_id, sr.provider_id}:
        raise HTTPException(status_code=403, detail="Not part of this request.")
    return create_message(db, sender_id=me.id, request_id=request_id, content=payload.content)

@router.get("/{request_id}", response_model=List[MsgOut])
def get_thread(request_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db), me=Depends(get_current_user)):
    sr = get_sr(db, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found.")
    if me.id not in {sr.client_id, sr.provider_id}:
        raise HTTPException(status_code=403, detail="Not part of this request.")
    return list_messages(db, request_id, limit, offset)
