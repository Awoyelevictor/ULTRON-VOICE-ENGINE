# ULTRON Voice Engine

Standalone self-hostable TTS service for an original ULTRON-inspired synthetic voice.

## Workflow
1. Open `notebooks/ULTRON_Voice_Experiment.ipynb` in Google Colab.
2. Select a GPU runtime (T4 or better, when available).
3. Run the notebook to create and audition an original voice using Qwen3-TTS VoiceDesign.
4. If approved, generate a reusable speaker reference using Qwen3-TTS Base.
5. Put the generated WAV at `voice/ultron_profile/reference.wav` and its exact transcript in `reference.txt`.

This project is for an original synthetic character voice, not imitation of an identifiable actor or person. Do not use another person's voice without authorization.

## Models
- Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign
- Qwen/Qwen3-TTS-12Hz-1.7B-Base

Check the upstream model cards and repository for current model terms and requirements:
- https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign
- https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base
- https://github.com/QwenLM/Qwen3-TTS

## API setup
Python 3.10–3.12 recommended. Install dependencies in a clean environment:
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Set server environment variables:
```bash
ULTRON_API_KEY=generate-a-long-random-secret
ULTRON_REFERENCE_AUDIO=voice/ultron_profile/reference.wav
ULTRON_REFERENCE_TEXT=exact words spoken in reference.wav
```

Start:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`GET /health` checks service status. `POST /v1/audio/speech` accepts JSON `{"text":"Systems online.","language":"English"}` and returns WAV audio. Supply `Authorization: Bearer YOUR_KEY`.

## Compute reality
The 1.7B model requires a suitable GPU and substantial VRAM. A small CPU-only free web host (including typical free Render instances) is not suitable for inference. Free Colab/GPU platforms have availability, queue, and session limits; this project does not bypass them. A lightweight API gateway can be hosted separately from the GPU inference worker.

Never commit API keys, .env files, private recordings, or generated private voice assets.
