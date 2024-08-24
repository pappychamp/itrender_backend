from datetime import date
from itertools import groupby
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db
from src.schemas.trend import TrendListResponse
from src.services.trend import get_trend_data

router = APIRouter()


@router.get("/trend", response_model=Dict[str, List[TrendListResponse]])
async def list_trend(site: str, filter_date: date, session: AsyncSession = Depends(get_db)):
    response = await get_trend_data(site, filter_date, session)
    grouped_data = {}
    for site_name, items in groupby(response, key=lambda x: x.site.name):
        grouped_data[site_name] = list(items)
    return grouped_data
