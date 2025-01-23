from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import BasicResponse, AddUserBody
from repositories.api import ApiRepository


async def check_user(db : AsyncSession, telegram_id: int) -> BasicResponse:
    response = await ApiRepository.check(db, telegram_id)
    return response