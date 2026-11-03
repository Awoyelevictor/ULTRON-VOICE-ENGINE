import os
from pathlib import Path
import torch
from qwen_tts import Qwen3TTSModel

MODEL_ID = os.getenv("ULTRON_MODEL_ID", "Qwen/Qwen3-TTS-12Hz-1.7B-Base")
REFERENCE_AUDIO = Path(os.getenv("ULTRON_REFERENCE_AUDIO", "voice/ultron_profile/reference.wav"))
REFERENCE_TEXT = os.getenv("ULTRON_REFERENCE_TEXT", "Systems online. I have reviewed the available data.")
_model = None
_voice_prompt = None

def engine_status():
    return {"model": MODEL_ID, "model_loaded": _model is not None,
            "gpu_available": torch.cuda.is_available(),
            "reference_audio_found": REFERENCE_AUDIO.exists()}

def _load():
    global _model, _voice_prompt
    if _model is not None:
        return _model, _voice_prompt
    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA GPU is required for this inference configuration.")
    if not REFERENCE_AUDIO.exists():
        raise RuntimeError(f"Voice reference not found: {REFERENCE_AUDIO}")
    capability = torch.cuda.get_device_capability()
    dtype = torch.bfloat16 if capability[0] >= 8 else torch.float16
    _model = Qwen3TTSModel.from_pretrained(
        MODEL_ID, device_map="cuda:0", dtype=dtype, attn_implementation="sdpa")
    _voice_prompt = _model.create_voice_clone_prompt(
        ref_audio=str(REFERENCE_AUDIO), ref_text=REFERENCE_TEXT)
    return _model, _voice_prompt

def synthesize(text: str, language: str = "English"):
    model, prompt = _load()
    wavs, sample_rate = model.generate_voice_clone(
        text=text, language=language, voice_clone_prompt=prompt,
        non_streaming_mode=True)
    return wavs[0], sample_rate
