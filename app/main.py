# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.errors import install_error_handlers
from app.routers import auth, users, service_requests, messages

# Create DB tables on startup (OK for dev; for prod use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="2U Backend API",
    description="On-road assistance platform: users, providers, requests, and chat.",
    version="1.0.0",
)

# Global error handlers
install_error_handlers(app)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(service_requests.router)
app.include_router(messages.router)

@app.get("/", tags=["Health"])
def root():
    return {"ok": True, "service": "2U API"}
