from datetime import date
from typing import List

from sqlalchemy import and_, desc, or_, select
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.trend import Site, Tag, TrendData


async def get_all_site_trend_data(filter_date: date, session: AsyncSession) -> List[TrendData]:
    try:
        result: Result = await session.execute(
            select(TrendData).join(TrendData.site).options(joinedload(TrendData.site), joinedload(TrendData.tags)).filter(TrendData.created_at == filter_date).order_by(Site.name, TrendData.ranking)
        )
        response = result.scalars().unique().all()
        return response
    except SQLAlchemyError:
        raise
    except Exception:
        raise


async def get_site_trend_data(site_name: str, filter_date: date, session: AsyncSession) -> List[TrendData]:
    try:
        result: Result = await session.execute(
            select(TrendData)
            .join(TrendData.site)
            .options(joinedload(TrendData.site), joinedload(TrendData.tags))
            .filter(Site.name == site_name, TrendData.created_at == filter_date)
            .order_by(TrendData.ranking)
        )
        response = result.scalars().unique().all()
        return response
    except SQLAlchemyError:
        raise
    except Exception:
        raise


async def get_latest_date(session: AsyncSession) -> date:
    try:
        # TrendDataの中で最新の日付を取得
        latest_date_subquery: Result = await session.execute(select(TrendData.created_at).order_by(TrendData.created_at.desc()).limit(1))
        latest_date = latest_date_subquery.scalar()
        return latest_date
    except SQLAlchemyError:
        raise
    except Exception:
        raise


async def get_filter_word_trend_data(filter_words: List[str], session: AsyncSession) -> List[TrendData]:
    try:
        # tz = pytz.timezone("Asia/Tokyo")
        # start_of_day = tz.localize(datetime(filter_date.year, filter_date.month, filter_date.day))
        # end_of_day = start_of_day + timedelta(days=1)
        result: Result = await session.execute(
            select(TrendData)
            .join(TrendData.site)
            .outerjoin(TrendData.tags)
            .options(joinedload(TrendData.site), joinedload(TrendData.tags))
            # filter_wordsのすべての単語について、TrendData.titleまたはTag.nameまたはSite.nameにその単語が含まれている場合に結果を取得
            .filter(
                and_(
                    *[
                        # fileter_wordの部分一致かつ大文字小文字区別しない
                        or_(
                            TrendData.title.ilike(f"%{filter_word}%"),
                            Tag.name.ilike(f"%{filter_word}%"),
                            Site.name.ilike(f"%{filter_word}%"),
                        )
                        for filter_word in filter_words
                    ]
                )
            )
            # レコードの新しい順に
            .order_by(desc(TrendData.created_at))
        )
        # タイトル重複を削除
        seen_titles = set()  # titleを一意に管理するためのセット
        response = []  # 重複を除いたTrendDataを格納するリスト

        for trend_data in result.scalars().unique().all():
            if trend_data.title not in seen_titles:
                response.append(trend_data)  # 一意な要素のみリストに追加
                seen_titles.add(trend_data.title)  # titleをセットに追加

        return response
    except SQLAlchemyError:
        raise
    except Exception:
        raise
