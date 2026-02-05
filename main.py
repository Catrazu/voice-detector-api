import base64
import uuid
import os
import requests

from fastapi import FastAPI, Depends, HTTPException

from auth import verify_api_key
from audio_utils import convert_mp3_to_wav
from features import extract_mfcc_features
from schemas import DetectionResponse

# ---------------------------------------------------
# Create FastAPI App  (IMPORTANT)
# ---------------------------------------------------

app = FastAPI(
    title="AI Voice Detection API",
    description="Detect AI-generated vs Human voice",
    version="1.0"
)

# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------

@app.get("/")
def root():
    return {"message": "AI Voice Detection API Running"}

# ---------------------------------------------------
# Detect Endpoint
# ---------------------------------------------------

@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: dict,
    api_key: str = Depends(verify_api_key)
):

    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]

    language = data.get("language")

    if language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Accept many possible key names
    audio_base64 = (
        data.get("audio_base64")
        or data.get("audio_base64_format")
        or data.get("audioBase64Format")
        or data.get("AudioBase64Format")
        or data.get("Audio Base64 Format")
    )

    audio_url = data.get("audio_url")

    # -------------------------------
    # Case 1: Base64 Audio
    # -------------------------------
    if audio_base64:
        try:
            audio_bytes = base64.b64decode(audio_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # -------------------------------
    # Case 2: Audio URL
    # -------------------------------
    elif audio_url:
        try:
            response = requests.get(audio_url)
            audio_bytes = response.content
        except Exception:
            raise HTTPException(status_code=400, detail="Unable to download audio")

    else:
        raise HTTPException(status_code=400, detail="Provide audio_base64 or audio_url")

    # -------------------------------
    # Save MP3
    # -------------------------------
    mp3_file = f"audio_{uuid.uuid4()}.mp3"

    with open(mp3_file, "wb") as f:
        f.write(audio_bytes)

    # Convert to WAV
    wav_file = convert_mp3_to_wav(mp3_file)

    # Extract Features
    mfccs = extract_mfcc_features(wav_file)

    # -------------------------------
    # Simple Rule-Based Classifier
    # -------------------------------
    if mfccs.var() > 1000:
        result = "HUMAN"
        confidence = 0.95
        explanation = "Higher MFCC variance and natural spectral variation indicate human voice"
    else:
        result = "AI_GENERATED"
        confidence = 0.85
        explanation = "Lower spectral variance indicates synthetic voice patterns"

    # Cleanup
    try:
        os.remove(mp3_file)
        os.remove(wav_file)
    except:
        pass

    return DetectionResponse(
        result=result,
        confidence=confidence,
        language=language,
        explanation=explanation
    )











