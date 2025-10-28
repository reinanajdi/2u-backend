@'
import traceback
try:
    from app.main import app
except Exception:
    tb = traceback.format_exc()
    from fastapi import FastAPI
    app = FastAPI(title="Boot Error")
    @app.get("/")
    def _boot_error():
        return {"error": "boot_failed", "traceback": tb}
'@ | Out-File -Encoding UTF8 index.py
