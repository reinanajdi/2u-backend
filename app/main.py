# app/main.py
from fastapi import FastAPI
from app.database import engine, Base, DATABASE_URL
from app.errors import install_error_handlers
from app.routers import auth, users, service_requests, messages

app = FastAPI(
    title="2U Backend API",
    description="On-road assistance platform: users, providers, requests, and chat.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    try:
        if DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
            # 👇 import your ORM models so metadata is populated
            from app import models  # noqa: F401
            Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Startup DB init skipped/failed:", e)

install_error_handlers(app)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(service_requests.router)
app.include_router(messages.router)

@app.get("/", tags=["Health"])
def root():
    return {"ok": True, "service": "2U API"}
