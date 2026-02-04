import base64
import uuid

from fastapi import FastAPI, Depends, HTTPException
from schemas import AudioRequest, DetectionResponse
from auth import verify_api_key
from audio_utils import convert_mp3_to_wav
from features import extract_mfcc_features

app = FastAPI(
    title="AI Voice Detection API",
    description="Detect AI-generated vs Human voice from Base64 audio",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "AI Voice Detection API Running"}

@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: AudioRequest,
    api_key: str = Depends(verify_api_key)
):
    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]

    if data.language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    try:
        audio_bytes = base64.b64decode(data.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    mp3_file = f"audio_{uuid.uuid4()}.mp3"

    with open(mp3_file, "wb") as f:
        f.write(audio_bytes)

    wav_file = convert_mp3_to_wav(mp3_file)

    mfccs = extract_mfcc_features(wav_file)

    if mfccs.var() > 1000:
        result = "HUMAN"
        confidence = 0.95
        explanation = "Higher MFCC variance and natural spectral variation indicate human voice"
    else:
        result = "AI_GENERATED"
        confidence = 0.85
        explanation = "Lower spectral variance indicates synthetic voice patterns"

    return DetectionResponse(
        result=result,
        confidence=confidence,
        language=data.language,
        explanation=explanation
    )






