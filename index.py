from fastapi import FastAPI`napp = FastAPI()`n@app.get("/")`ndef ok():`n    return {"ok": True}
