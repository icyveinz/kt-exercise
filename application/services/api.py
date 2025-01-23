import os
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import BasicResponse, AddUserBody
from repositories.api import ApiRepository


class ApiService:
    @staticmethod
    async def check_user(db: AsyncSession, telegram_id: int) -> BasicResponse:
        response = await ApiRepository.check(db, telegram_id)
        return response

    @staticmethod
    async def add_user(db: AsyncSession, application: AddUserBody) -> BasicResponse:
        try:
            TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
            if TELEGRAM_BOT_TOKEN == application.telegram_bot_token:
                response = await ApiRepository.insert_user(db, application)
                return response
            else:
                return BasicResponse(
                    is_succeeded=False, additional_info="Your token doesn't match."
                )
        except Exception as e:
            return BasicResponse(is_succeeded=False, additional_info=str(e))
