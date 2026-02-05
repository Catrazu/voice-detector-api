from fastapi import Header, HTTPException

API_KEY = "mysecretkey"

def verify_api_key(
    x_api_key: str = Header(None),
    authorization: str = Header(None)
):
    if x_api_key == API_KEY:
        return x_api_key

    if authorization:
        token = authorization.replace("Bearer ", "")
        if token == API_KEY:
            return token

    raise HTTPException(status_code=401, detail="Not authenticated")
