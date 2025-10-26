from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, RequestStatus

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: UserRole = UserRole.client
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_available: bool = True

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class SRBase(BaseModel):
    description: str = Field(..., min_length=3, max_length=2000)
    latitude: float
    longitude: float

class SRCreate(SRBase):
    pass

class SROut(SRBase):
    id: int
    client_id: int
    provider_id: Optional[int] = None
    status: RequestStatus
    created_at: datetime
    class Config:
        from_attributes = True

class MsgCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)

class MsgOut(BaseModel):
    id: int
    sender_id: int
    request_id: int
    content: str
    timestamp: datetime
    class Config:
        from_attributes = True
