import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import BasicResponse
from repositories.api import ApiRepository
from services.api import ApiService


@pytest.mark.asyncio
@patch.object(ApiRepository, "check", new_callable=AsyncMock)
async def test_check_user_exists(mock_check):
    # Prepare mock data
    mock_response = BasicResponse(is_succeeded=True, additional_info="User exists")
    mock_check.return_value = mock_response

    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Call the service method
    response = await ApiService.check_user(mock_db, telegram_id=12345)

    # Assert the response
    assert response.is_succeeded is True
    assert response.additional_info == "User exists"


@pytest.mark.asyncio
@patch.object(ApiRepository, "check", new_callable=AsyncMock)
async def test_check_user_not_exists(mock_check):
    # Prepare mock data
    mock_response = BasicResponse(
        is_succeeded=False, additional_info="User does not exist"
    )
    mock_check.return_value = mock_response

    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Call the service method
    response = await ApiService.check_user(mock_db, telegram_id=12345)

    # Assert the response
    assert response.is_succeeded is False
    assert response.additional_info == "User does not exist"


@pytest.mark.asyncio
@patch.object(ApiRepository, "check", new_callable=AsyncMock)
async def test_check_user_exception(mock_check):
    # Prepare mock data
    mock_check.side_effect = Exception("Database error")

    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Call the service method
    response = await ApiService.check_user(mock_db, telegram_id=12345)

    # Assert the response
    assert response.is_succeeded is False
    assert response.additional_info == "Database error"
