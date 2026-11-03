from fastapi import APIRouter
from app.services.tts_engine import engine_status

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "ultron-voice-engine", **engine_status()}
