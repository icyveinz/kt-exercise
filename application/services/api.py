import os

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import (
    BasicResponse,
    AddUserBody,
    CheckImeiBody,
    CheckImeiResponse,
    AdditionalInfo,
)
from repositories.api import ApiRepository


class ApiService:
    @staticmethod
    async def check_imei(application: CheckImeiBody) -> CheckImeiResponse:
        try:
            ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
            if ACCESS_TOKEN == application.token:
                url = "https://api.imeicheck.net/v1/checks"
                headers = {
                    "Authorization": f"Bearer {os.getenv('THENEO_TOKEN')}",
                    "Accept-Language": "en",
                    "Content-Type": "application/json",
                }
                data = {"deviceId": f"{application.imei}", "serviceId": 22}
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, headers=headers, json=data
                    ) as response:
                        response.raise_for_status()  # Проверка на ошибки HTTP
                        result = await response.json()
                        properties = result.get("properties", {})
                        additional_info = AdditionalInfo(**properties)
                        return CheckImeiResponse(
                            is_succeeded=True, additional_info=additional_info
                        )
            else:
                return CheckImeiResponse(
                    is_succeeded=False, additional_info="Invalid access token"
                )
        except aiohttp.ClientError as e:
            return CheckImeiResponse(
                is_succeeded=False, additional_info={"error": str(e)}
            )
        except Exception as e:
            return CheckImeiResponse(
                is_succeeded=False, additional_info={"error": str(e)}
            )

    @staticmethod
    async def add_user(db: AsyncSession, application: AddUserBody) -> BasicResponse:
        try:
            ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
            if ACCESS_TOKEN == application.token:
                response = await ApiRepository.insert_user(db, application)
                return response
            else:
                return BasicResponse(
                    is_succeeded=False, additional_info="Your token doesn't match."
                )
        except Exception as e:
            return BasicResponse(is_succeeded=False, additional_info=str(e))

    @staticmethod
    async def check_user(db: AsyncSession, telegram_id: int) -> BasicResponse:
        response = await ApiRepository.check(db, telegram_id)
        return response
