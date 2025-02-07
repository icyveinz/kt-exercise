import pytest
from unittest.mock import AsyncMock, patch
from core.schemas import CheckImeiBody, CheckImeiResponse, AdditionalInfo
from clients.api import ImeiCheckClient  # Import the ImeiCheckClient
from services.api import ApiService

@pytest.mark.asyncio
@patch.object(ImeiCheckClient, 'check_imei', new_callable=AsyncMock)
async def test_check_imei_success(mock_check_imei):
    # Prepare mock data with a valid IMEI
    application = CheckImeiBody(imei="490154203237518")  # Valid IMEI number
    mock_response = CheckImeiResponse(is_succeeded=True, additional_info="IMEI is valid", result=None)
    mock_check_imei.return_value = mock_response

    # Call the service method
    response = await ApiService.check_imei(application)

    # Assert the response
    assert response.is_succeeded is True
    assert response.additional_info == "IMEI is valid"



@pytest.mark.asyncio
@patch.object(ImeiCheckClient, 'check_imei', new_callable=AsyncMock)
async def test_check_imei_failure(mock_check_imei):
    # Prepare mock data
    application = CheckImeiBody(imei="490154203237518")
    mock_response = CheckImeiResponse(is_succeeded=False, additional_info="IMEI is invalid", result=None)
    mock_check_imei.return_value = mock_response

    # Call the service method
    response = await ApiService.check_imei(application)

    # Assert the response
    assert response.is_succeeded is False
    assert response.additional_info == "IMEI is invalid"
    assert response.result is None


@pytest.mark.asyncio
@patch.object(ImeiCheckClient, 'check_imei', new_callable=AsyncMock)
async def test_check_imei_exception(mock_check_imei):
    # Prepare mock data
    application = CheckImeiBody(imei="490154203237518")
    mock_check_imei.side_effect = Exception("API error")

    # Call the service method
    response = await ApiService.check_imei(application)

    # Assert the response
    assert response.is_succeeded is False
    assert response.additional_info == "API error"
    assert response.result is None
