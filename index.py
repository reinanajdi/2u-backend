# index.py
try:
    from app.main import app
except Exception as e:
    # Fallback: expose the import error at "/" so you can see it in logs
    from fastapi import FastAPI
    app = FastAPI(title="Boot Error")
    @app.get("/")
    def _boot_error():
        return {"error": "boot_failed", "detail": str(e)}
