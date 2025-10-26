from sqlalchemy.orm import Session
from app.models import Message

def create_message(db: Session, *, sender_id, request_id, content):
    m = Message(sender_id=sender_id, request_id=request_id, content=content)
    db.add(m); db.commit(); db.refresh(m); return m

def list_messages(db: Session, request_id: int, limit=100, offset=0):
    return (db.query(Message)
              .filter(Message.request_id == request_id)
              .order_by(Message.timestamp.asc())
              .offset(offset).limit(limit).all())
