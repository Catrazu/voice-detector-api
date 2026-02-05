from pydantic import BaseModel
from typing import Optional

class AudioRequest(BaseModel):
    audio_base64: Optional[str] = None
    audio_url: Optional[str] = None
    language: str

class DetectionResponse(BaseModel):
    result: str
    confidence: float
    language: str
    explanation: str


