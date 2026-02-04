import base64
import uuid
import numpy as np
from fastapi import FastAPI, Depends, HTTPException

from schemas import AudioRequest, DetectionResponse
from auth import verify_api_key
from audio_utils import convert_mp3_to_wav
from features import extract_mfcc_features

app = FastAPI(title="AI Voice Detection API")


@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: AudioRequest,
    auth: str = Depends(verify_api_key)
):
    # 1️⃣ Validate language
    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]
    if data.language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # 2️⃣ Decode Base64 audio
    try:
        audio_bytes = base64.b64decode(data.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # 3️⃣ Save MP3 file
    mp3_file = f"test_audio_{uuid.uuid4()}.mp3"
    with open(mp3_file, "wb") as f:
        f.write(audio_bytes)

    # 4️⃣ Convert MP3 → WAV
    try:
        wav_file = convert_mp3_to_wav(mp3_file)
    except Exception:
        raise HTTPException(status_code=500, detail="MP3 to WAV conversion failed")

    # 5️⃣ Extract MFCC features
    try:
        mfcc_features = extract_mfcc_features(wav_file)
    except Exception:
        raise HTTPException(status_code=500, detail="MFCC feature extraction failed")

    # 6️⃣ AI vs HUMAN detection logic (EXPLAINABLE)
    mfcc_variance = np.var(mfcc_features)
    mfcc_mean_abs = np.mean(np.abs(mfcc_features))

    if mfcc_variance < 500 and mfcc_mean_abs < 800:
        result = "AI_GENERATED"
        confidence = round(min(0.95, 0.65 + (500 - mfcc_variance) / 1000), 2)
        explanation = "Low MFCC variance and smooth spectral features indicate AI-generated voice"
    else:
        result = "HUMAN"
        confidence = round(min(0.95, 0.65 + (mfcc_variance - 500) / 1000), 2)
        explanation = "Higher MFCC variance and natural spectral variation indicate human voice"

    # 7️⃣ Final structured response
    return DetectionResponse(
        result=result,
        confidence=confidence,
        language=data.language,
        explanation=explanation
    )





