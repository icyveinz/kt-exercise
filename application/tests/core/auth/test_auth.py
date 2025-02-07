import os
import pytest
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from core.auth.auth import validate_token, get_current_user


@pytest.fixture
def valid_token():
    return "valid_token"

@pytest.fixture
def invalid_token():
    return "invalid_token"

@pytest.fixture(autouse=True)
def set_env_token(valid_token):
    os.environ["ACCESS_TOKEN"] = valid_token

# Test validate_token function
def test_validate_token(valid_token, invalid_token):
    assert validate_token(valid_token) is True
    assert validate_token(invalid_token) is False

# Test get_current_user function with a valid token
@pytest.mark.asyncio
async def test_get_current_user_valid_token(valid_token):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=valid_token)
    token = await get_current_user(credentials)
    assert token == valid_token

# Test get_current_user function with an invalid token
@pytest.mark.asyncio
async def test_get_current_user_invalid_token(invalid_token):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(credentials)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid or expired token"