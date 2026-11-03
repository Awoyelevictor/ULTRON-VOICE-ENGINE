import os
import secrets
from fastapi import Header, HTTPException

def require_api_key(authorization: str | None = Header(default=None)):
    expected = os.getenv("ULTRON_API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="ULTRON_API_KEY is not configured")
    scheme, _, supplied = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True
