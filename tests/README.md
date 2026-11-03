# Tests

After configuring a GPU and a generated reference WAV:
- GET /health should return 200.
- POST /v1/audio/speech without a Bearer token should return 401.
- An authenticated speech request should return audio/wav.

Model inference tests require GPU resources and are intentionally not run in basic CI.
