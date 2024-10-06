from datetime import date
from itertools import groupby
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db
from src.logs.logs_setting import logger
from src.schemas.trend import TrendListResponse
from src.services.trend import (
    get_all_site_trend_data,
    get_filter_word_trend_data,
    get_latest_date,
    get_site_trend_data,
)

router = APIRouter()


@router.get("/trend", response_model=Dict[date, Dict[str, List[TrendListResponse]]])
async def list_latest_trend(session: AsyncSession = Depends(get_db)):
    try:
        filter_date = await get_latest_date(session)
        response = await get_all_site_trend_data(filter_date, session)
        grouped_data = {}
        for site_name, items in groupby(response, key=lambda x: x.site.name):
            grouped_data[site_name] = list(items)
        return {filter_date: grouped_data}
    except Exception as e:
        logger.error(f"{str(e)}")
        raise HTTPException(status_code=500, detail={})


@router.get("/trend/{site_name}", response_model=List[TrendListResponse])
async def list_site_trend(site_name: str, filter_date: date, session: AsyncSession = Depends(get_db)):
    try:
        response = await get_site_trend_data(site_name, filter_date, session)
        return response
    except Exception as e:
        logger.error(f"{str(e)}")
        raise HTTPException(status_code=500, detail={})


@router.get("/search", response_model=Page[TrendListResponse])
async def search_words_trend(
    q: Annotated[list[str], Query(max_length=3)],
    size: int = Query(20, description="Number of items per page"),
    page: int = Query(1, description="Page number"),
    session: AsyncSession = Depends(get_db),
):
    try:
        response = await get_filter_word_trend_data(q, session)
        return paginate(response, Params(size=size, page=page))
    except Exception as e:
        logger.error(f"{str(e)}")
        raise HTTPException(status_code=500, detail={})
