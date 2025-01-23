import aiohttp
from core.schemas import CheckImeiResponse, AdditionalInfo


class ImeiCheckClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.imeicheck.net/v1/checks"

    async def check_imei(self, imei: str) -> CheckImeiResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept-Language": "en",
            "Content-Type": "application/json"
        }
        data = {
            "deviceId": imei,
            "serviceId": 22
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    properties = result.get("properties", {})
                    additional_info = AdditionalInfo(**properties)
                    return CheckImeiResponse(
                        is_succeeded=True, additional_info=additional_info
                    )
        except aiohttp.ClientError as e:
            return CheckImeiResponse(
                is_succeeded=False, additional_info={"error": str(e)}
            )
        except Exception as e:
            return CheckImeiResponse(
                is_succeeded=False, additional_info={"error": str(e)}
            )