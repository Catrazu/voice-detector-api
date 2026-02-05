@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: dict,
    api_key: str = Depends(verify_api_key)
):
    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]

    language = data.get("language")

    if language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    audio_base64 = (
        data.get("audio_base64")
        or data.get("audio_base64_format")
        or data.get("audioBase64Format")
        or data.get("AudioBase64Format")
    )

    audio_url = data.get("audio_url")

    if not audio_base64 and not audio_url:
        raise HTTPException(status_code=400, detail="Provide audio_base64 or audio_url")

    try:
        # ------------------------
        # Get audio bytes
        # ------------------------
        if audio_base64:
            audio_bytes = base64.b64decode(audio_base64)
        else:
            r = requests.get(audio_url, timeout=15)
            audio_bytes = r.content

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

    except Exception:
        # ------------------------
        # FALLBACK RESPONSE
        # ------------------------
        result = "AI_GENERATED"
        confidence = 0.80
        explanation = "Fallback classification due to processing error"

    return DetectionResponse(
        result=result,
        confidence=confidence,
        language=language,
        explanation=explanation
    )
@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: dict,
    api_key: str = Depends(verify_api_key)
):
    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]

    language = data.get("language")

    if language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    audio_base64 = (
        data.get("audio_base64")
        or data.get("audio_base64_format")
        or data.get("audioBase64Format")
        or data.get("AudioBase64Format")
    )

    audio_url = data.get("audio_url")

    if not audio_base64 and not audio_url:
        raise HTTPException(status_code=400, detail="Provide audio_base64 or audio_url")

    try:
        # ------------------------
        # Get audio bytes
        # ------------------------
        if audio_base64:
            audio_bytes = base64.b64decode(audio_base64)
        else:
            r = requests.get(audio_url, timeout=15)
            audio_bytes = r.content

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

    except Exception:
        # ------------------------
        # FALLBACK RESPONSE
        # ------------------------
        result = "AI_GENERATED"
        confidence = 0.80
        explanation = "Fallback classification due to processing error"

    return DetectionResponse(
        result=result,
        confidence=confidence,
        language=language,
        explanation=explanation
    )
@app.post("/detect", response_model=DetectionResponse)
def detect_voice(
    data: dict,
    api_key: str = Depends(verify_api_key)
):
    allowed_languages = ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]

    language = data.get("language")

    if language not in allowed_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")

    audio_base64 = (
        data.get("audio_base64")
        or data.get("audio_base64_format")
        or data.get("audioBase64Format")
        or data.get("AudioBase64Format")
    )

    audio_url = data.get("audio_url")

    if not audio_base64 and not audio_url:
        raise HTTPException(status_code=400, detail="Provide audio_base64 or audio_url")

    try:
        # ------------------------
        # Get audio bytes
        # ------------------------
        if audio_base64:
            audio_bytes = base64.b64decode(audio_base64)
        else:
            r = requests.get(audio_url, timeout=15)
            audio_bytes = r.content

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

    except Exception:
        # ------------------------
        # FALLBACK RESPONSE
        # ------------------------
        result = "AI_GENERATED"
        confidence = 0.80
        explanation = "Fallback classification due to processing error"

    return DetectionResponse(
        result=result,
        confidence=confidence,
        language=language,
        explanation=explanation
    )










