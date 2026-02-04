from fastapi import Header, HTTPException

API_KEY = "demo_api_key_123"

def verify_api_key(
    authorization: str = Header(None),
    Authorization: str = Header(None)
):
    token = Authorization or authorization

    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if token != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key")

    return token


