from sqlalchemy.orm import Session
from app.models import ServiceRequest, RequestStatus

def create_request(db: Session, *, client_id, description, lat, lon):
    sr = ServiceRequest(client_id=client_id, description=description, latitude=lat, longitude=lon)
    db.add(sr); db.commit(); db.refresh(sr); return sr

def assign_provider(db: Session, *, sr_id, provider_id):
    sr = db.get(ServiceRequest, sr_id)
    if not sr: return None
    sr.provider_id = provider_id; sr.status = RequestStatus.accepted
    db.commit(); db.refresh(sr); return sr

def update_status(db: Session, *, sr_id, status: RequestStatus):
    sr = db.get(ServiceRequest, sr_id); 
    if not sr: return None
    sr.status = status; db.commit(); db.refresh(sr); return sr

def get_by_id(db: Session, sr_id: int):
    return db.get(ServiceRequest, sr_id)

def list_for_user(db: Session, *, client_id: int | None = None, provider_id: int | None = None, limit=50, offset=0):
    q = db.query(ServiceRequest)
    if client_id: q = q.filter(ServiceRequest.client_id == client_id)
    if provider_id: q = q.filter(ServiceRequest.provider_id == provider_id)
    return q.order_by(ServiceRequest.created_at.desc()).offset(offset).limit(limit).all()
