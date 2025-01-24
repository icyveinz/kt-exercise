from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_current_user
from core.database import SessionLocal
from core.schemas import CheckImeiResponse, BasicResponse, CheckImeiBody, AddUserBody
from services.api import ApiService

router = APIRouter(prefix="/api", tags=["api"])


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/check-imei", response_model=CheckImeiResponse)
async def check_imei_route(
    application: CheckImeiBody,
    credentials: HTTPAuthorizationCredentials = Depends(get_current_user),
):
    try:
        return await ApiService.check_imei(application)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add-user", response_model=BasicResponse)
async def add_user_route(
    application: AddUserBody,
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(get_current_user),
):
    try:
        return await ApiService.add_user(db, application)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/check-user", response_model=BasicResponse)
async def check_user_route(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await ApiService.check_user(db, telegram_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
