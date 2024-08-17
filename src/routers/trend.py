from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db
from src.schemas.trend import TrendListResponse
from src.services.trend import get_trend_data

router = APIRouter()


@router.get("/trend", response_model=List[TrendListResponse])
async def list_trend(site: str, filter_date: date, session: AsyncSession = Depends(get_db)):
    response = await get_trend_data(site, filter_date, session)
    return response
