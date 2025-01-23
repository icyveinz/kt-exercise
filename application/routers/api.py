from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import SessionLocal
from core.schemas import CheckImeiResponse, BasicResponse, CheckImeiBody, AddUserBody

router = APIRouter(prefix="/api", tags=["api"])


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/check-imei", response_model=CheckImeiResponse)
async def create(application: CheckImeiBody, db: AsyncSession = Depends(get_db)):
    try:
        return await create_application(application, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add-user", response_model=BasicResponse)
async def create(application: AddUserBody, db: AsyncSession = Depends(get_db)):
    try:
        return await create_application(application, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/check-user", response_model=BasicResponse)
async def create(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await create_application(application, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
