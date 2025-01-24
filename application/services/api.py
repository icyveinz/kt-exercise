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
            client = ImeiCheckClient(api_key=os.getenv("THENEO_TOKEN"))
            result = await client.check_imei(imei=application.imei)
            return result
        except Exception as e:
            return CheckImeiResponse(
                is_succeeded=False, additional_info=str(e), result=None
            )

    @staticmethod
    async def add_user(db: AsyncSession, application: AddUserBody) -> BasicResponse:
        try:
            response = await ApiRepository.insert_user(db, application)
            return response
        except Exception as e:
            return BasicResponse(is_succeeded=False, additional_info=str(e))

    @staticmethod
    async def check_user(db: AsyncSession, telegram_id: int) -> BasicResponse:
        response = await ApiRepository.check(db, telegram_id)
        return response
