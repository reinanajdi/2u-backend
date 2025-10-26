from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    client = "client"
    provider = "provider"

class RequestStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.client)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    client_requests = relationship("ServiceRequest", back_populates="client", foreign_keys="ServiceRequest.client_id")
    provider_requests = relationship("ServiceRequest", back_populates="provider", foreign_keys="ServiceRequest.provider_id")

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), default=RequestStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client = relationship("User", foreign_keys=[client_id], back_populates="client_requests")
    provider = relationship("User", foreign_keys=[provider_id], back_populates="provider_requests")
    messages = relationship("Message", back_populates="request", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    request_id: Mapped[int] = mapped_column(ForeignKey("service_requests.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sender = relationship("User")
    request = relationship("ServiceRequest", back_populates="messages")
