import os
from sqlalchemy.ext.asyncio import AsyncSession
from clients.api import ImeiCheckClient
from core.schemas import (
    BasicResponse,
    AddUserBody,
    CheckImeiBody,
    CheckImeiResponse,
)
from repositories.api import ApiRepository


class ApiService:
    @staticmethod
    async def check_imei(application: CheckImeiBody) -> CheckImeiResponse:
        try:
            ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
            if ACCESS_TOKEN == application.token:
                client = ImeiCheckClient(api_key=os.getenv('THENEO_TOKEN'))
                result = await client.check_imei(imei=application.imei)
                return result
            else:
                return CheckImeiResponse(
                    is_succeeded=False, additional_info="Invalid access token"
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
