from io import BytesIO
import soundfile as sf
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from app.security.authentication import require_api_key
from app.services.tts_engine import synthesize

router = APIRouter()

class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    language: str = "English"

@router.post("/audio/speech", dependencies=[Depends(require_api_key)])
def create_speech(payload: SpeechRequest):
    try:
        wav, sample_rate = synthesize(payload.text, payload.language)
        buffer = BytesIO()
        sf.write(buffer, wav, sample_rate, format="WAV", subtype="PCM_16")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="audio/wav",
            headers={"Content-Disposition": 'inline; filename="ultron.wav"'})
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Speech generation failed: {exc}")
