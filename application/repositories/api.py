from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Application
from core.schemas import BasicResponse, AddUserBody


class ApiRepository:
    @staticmethod
    async def check(db: AsyncSession, telegram_id: int) -> BasicResponse:
        try:
            query = select(Application).where(Application.telegram_id == telegram_id)
            result = await db.execute(query)
            application = result.scalar_one_or_none()
            if application:
                return BasicResponse(is_succeeded=True, additional_info="User exists")
            else:
                return BasicResponse(
                    is_succeeded=False, additional_info="User does not exist"
                )
        except Exception as e:
            return BasicResponse(is_succeeded=False, additional_info=str(e))

    @staticmethod
    async def insert_user(db: AsyncSession, application: AddUserBody) -> BasicResponse:
        try:
            new_user = Application(telegram_id=application.telegram_id)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return BasicResponse(
                is_succeeded=True,
                additional_info=f"User with id={application.telegram_id} is added to the db",
            )
        except Exception as e:
            return BasicResponse(is_succeeded=False, additional_info=str(e))
