import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

auth_scheme = HTTPBearer()

def validate_token(token: str) -> bool:
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    return ACCESS_TOKEN == token

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    if not validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return token