from datetime import date, datetime, timedelta
from typing import List

import pytz
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.trend import Site, TrendData


async def get_all_trend_data(filter_date: date, session: AsyncSession) -> List[TrendData]:
    tz = pytz.timezone("Asia/Tokyo")
    start_of_day = tz.localize(datetime(filter_date.year, filter_date.month, filter_date.day))
    end_of_day = start_of_day + timedelta(days=1)
    result: Result = await session.execute(
        select(TrendData)
        .join(TrendData.site)
        .options(joinedload(TrendData.site), joinedload(TrendData.tags))
        .filter(
            TrendData.created_at >= start_of_day,
            TrendData.created_at < end_of_day,
        )
        .order_by(Site.name, TrendData.ranking)
    )
    response = result.scalars().unique().all()
    return response


async def get_site_trend_data(site_name: str, filter_date: date, session: AsyncSession) -> List[TrendData]:
    tz = pytz.timezone("Asia/Tokyo")
    start_of_day = tz.localize(datetime(filter_date.year, filter_date.month, filter_date.day))
    end_of_day = start_of_day + timedelta(days=1)
    result: Result = await session.execute(
        select(TrendData)
        .join(TrendData.site)
        .options(joinedload(TrendData.site), joinedload(TrendData.tags))
        .filter(
            Site.name == site_name,
            TrendData.created_at >= start_of_day,
            TrendData.created_at < end_of_day,
        )
        .order_by(TrendData.ranking)
    )

    response = result.scalars().unique().all()
    return response
