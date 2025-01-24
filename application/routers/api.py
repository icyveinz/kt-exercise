from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth.auth import get_current_user
from core.database import SessionLocal
from core.schemas import CheckImeiResponse, BasicResponse, CheckImeiBody, AddUserBody
from services.api import ApiService

router = APIRouter(prefix="/api", tags=["api"])


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post(
    "/check-imei",
    response_model=CheckImeiResponse,
    summary="Проверить IMEI",
    description="Проверить IMEI и получить информацию по устройству в ответе на свой запрос.",
    tags=["IMEI"],
)
async def check_imei_route(
    application: CheckImeiBody,
    _: HTTPAuthorizationCredentials = Depends(get_current_user),
):
    try:
        return await ApiService.check_imei(application)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/add-user",
    response_model=BasicResponse,
    summary="Дать доступ пользователю для бота",
    description="Добавить пользователя по ID telegram чтобы он смог делать запросы в бот и получать на них ответ.",
    tags=["Users"],
)
async def add_user_route(
    application: AddUserBody,
    db: AsyncSession = Depends(get_db),
    _: HTTPAuthorizationCredentials = Depends(get_current_user),
):
    try:
        return await ApiService.add_user(db, application)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/check-user",
    response_model=BasicResponse,
    summary="Проверить пользователя на наличие доступа (Изолированная)",
    description="Проверить пользователя по ID telegram и принять решение может ли он делать запросы к боту или нет. Изолированна и обрабатывает запросы приходящие только от других контейнеров в сборке",
    tags=["Users"],
)
async def check_user_route(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await ApiService.check_user(db, telegram_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
