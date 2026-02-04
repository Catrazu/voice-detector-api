from pydantic import BaseModel

class AudioRequest(BaseModel):
    audio_base64: str
    language: str

class DetectionResponse(BaseModel):
    result: str
    confidence: float
    language: str
    explanation: str
