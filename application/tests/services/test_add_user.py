import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import AddUserBody, BasicResponse
from repositories.api import ApiRepository
from services.api import ApiService


@pytest.mark.asyncio
@patch.object(ApiRepository, 'insert_user', new_callable=AsyncMock)
async def test_add_user_success(mock_insert_user):
    # Prepare mock data
    application = AddUserBody(telegram_id=12345)
    mock_response = BasicResponse(is_succeeded=True, additional_info="User with id=12345 is added to the db")
    mock_insert_user.return_value = mock_response

    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Call the service method
    response = await ApiService.add_user(mock_db, application)

    # Assert the response
    assert response.is_succeeded is True
    assert response.additional_info == "User with id=12345 is added to the db"


@pytest.mark.asyncio
@patch.object(ApiRepository, 'insert_user', new_callable=AsyncMock)
async def test_add_user_failure(mock_insert_user):
    # Prepare mock data
    application = AddUserBody(telegram_id=12345)
    mock_response = BasicResponse(is_succeeded=False, additional_info="Database error")
    mock_insert_user.return_value = mock_response

    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Call the service method
    response = await ApiService.add_user(mock_db, application)

    # Assert the response
    assert response.is_succeeded is False
    assert response.additional_info == "Database error"


@pytest.mark.asyncio
@patch.object(ApiRepository, 'insert_user', new_callable=AsyncMock)
async def test_add_user_exception(mock_insert_user):
    # Prepare mock data
    application = AddUserBody(telegram_id=12345)
    mock_insert_user.side_effect = Exception("Internal server error")

    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Call the service method
    response = await ApiService.add_user(mock_db, application)

    # Assert the response
    assert response.is_succeeded is False
    assert response.additional_info == "Internal server error"
