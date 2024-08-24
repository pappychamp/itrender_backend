from datetime import date, timedelta
from itertools import groupby
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db
from src.schemas.trend import TrendListResponse
from src.services.trend import get_all_trend_data, get_site_trend_data

router = APIRouter()


@router.get("/trend", response_model=Dict[str, List[TrendListResponse]])
async def list_all_trend(filter_date: date, session: AsyncSession = Depends(get_db)):
    response = await get_all_trend_data(filter_date, session)
    while not response:
        filter_date = filter_date - timedelta(days=1)
        response = await get_all_trend_data(filter_date, session)
    grouped_data = {}
    for site_name, items in groupby(response, key=lambda x: x.site.name):
        grouped_data[site_name] = list(items)
    return grouped_data


@router.get("/trend/{site_name}", response_model=Dict[str, List[TrendListResponse]])
async def list_site_trend(site_name: str, filter_date: date, session: AsyncSession = Depends(get_db)):
    response = await get_site_trend_data(site_name, filter_date, session)
    grouped_data = {}
    for site_name, items in groupby(response, key=lambda x: x.site.name):
        grouped_data[site_name] = list(items)
    return grouped_data
