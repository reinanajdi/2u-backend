import traceback
try:
    from app.main import app
except Exception:
    tb = traceback.format_exc()
    from fastapi import FastAPI
    app = FastAPI(title="Boot Error")
    @app.get("/")
    def _boot_error():
        # show the real error so we can fix it quickly
        return {"error": "boot_failed", "traceback": tb}
