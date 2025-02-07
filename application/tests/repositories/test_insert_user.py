from unittest.mock import MagicMock, AsyncMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import AddUserBody
from repositories.api import ApiRepository


@pytest.mark.asyncio
async def test_insert_user_success(mocker):
    # Mock the database session
    mock_db = MagicMock(AsyncSession)

    # Mock async methods (add, commit, refresh) using AsyncMock
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()  # Mock async commit
    mock_db.refresh = AsyncMock()  # Mock async refresh

    application = AddUserBody(telegram_id=12345)

    # Call the insert_user method
    response = await ApiRepository.insert_user(mock_db, application)

    # Assert the response indicates success
    assert response.is_succeeded is True
    assert response.additional_info == "User with id=12345 is added to the db"


@pytest.mark.asyncio
async def test_insert_user_exception(mocker):
    # Mock the database session to raise an exception
    mock_db = MagicMock(AsyncSession)
    mock_db.add.side_effect = Exception("Database error")

    application = AddUserBody(telegram_id=12345)

    # Call the method
    response = await ApiRepository.insert_user(mock_db, application)

    # Assert the response indicates failure and the exception message
    assert response.is_succeeded is False
    assert response.additional_info == "Database error"
