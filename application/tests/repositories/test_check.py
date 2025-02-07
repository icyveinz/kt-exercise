import pytest
from unittest.mock import MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Application
from repositories.api import ApiRepository


@pytest.mark.asyncio
async def test_check_user_exists(mocker):
    # Mock the database session and query result
    mock_db = MagicMock(AsyncSession)
    mock_result = MagicMock()
    mock_db.execute.return_value = mock_result
    mock_result.scalar_one_or_none.return_value = Application(telegram_id=12345)

    # Call the method
    response = await ApiRepository.check(mock_db, telegram_id=12345)

    # Assert the response is successful and the correct message is returned
    assert response.is_succeeded is True
    assert response.additional_info == "User exists"


@pytest.mark.asyncio
async def test_check_user_does_not_exist(mocker):
    # Mock the database session and query result
    mock_db = MagicMock(AsyncSession)
    mock_result = MagicMock()
    mock_db.execute.return_value = mock_result
    mock_result.scalar_one_or_none.return_value = None

    # Call the method
    response = await ApiRepository.check(mock_db, telegram_id=12345)

    # Assert the response indicates user does not exist
    assert response.is_succeeded is False
    assert response.additional_info == "User does not exist"


@pytest.mark.asyncio
async def test_check_user_exception(mocker):
    # Mock the database session to raise an exception
    mock_db = MagicMock(AsyncSession)
    mock_db.execute.side_effect = Exception("Database error")

    # Call the method
    response = await ApiRepository.check(mock_db, telegram_id=12345)

    # Assert the response indicates failure and the exception message
    assert response.is_succeeded is False
    assert response.additional_info == "Database error"
