# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# If on Vercel and no DATABASE_URL is provided, use in-memory SQLite
default_sqlite = "sqlite://"
if not os.getenv("VERCEL"):
    default_sqlite = "sqlite:///./dev.db"

DATABASE_URL = getattr(settings, "DATABASE_URL", None) or os.getenv("DATABASE_URL", default_sqlite)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
