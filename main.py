import base64
import uuid
import os
import requests

from fastapi import FastAPI, Depends, HTTPException, Header
from schemas import AudioRequest, DetectionResponse
from audio_utils import convert_mp3_to_wav
from features import extract_mfcc_features

# ============================
# CONFIG
# ============================

API_KEY = "mysecretkey"   # you can change later

app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="Detect whether voice is AI-generated or Human",
    version="1.0"
)

# ============================
# AUTH
# ============================

from fastapi import Header

API_KEY = "mysecretkey"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


# ============================
# ROOT
# ============================

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "AI Voice Detection API is live"
    }

# ============================
# DETECTION ENDPOINT
# ============================

@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: AudioRequest,
    api_key: str = Depends(verify_api_key)
):
    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]

    if data.language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # --------- GET AUDIO ----------
    if data.audio_base64:
        try:
            audio_bytes = base64.b64decode(data.audio_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    elif data.audio_url:
        import requests
        try:
            r = requests.get(data.audio_url)
            audio_bytes = r.content
        except:
            raise HTTPException(status_code=400, detail="Invalid audio URL")

    else:
        raise HTTPException(status_code=400, detail="Provide audio_base64 or audio_url")

    # --------- SAVE FILE ----------
    mp3_file = f"audio_{uuid.uuid4()}.mp3"
    with open(mp3_file, "wb") as f:
        f.write(audio_bytes)

    wav_file = convert_mp3_to_wav(mp3_file)

    mfccs = extract_mfcc_features(wav_file)

    # --------- CLASSIFICATION ----------
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







