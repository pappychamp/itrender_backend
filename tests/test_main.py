import uuid
from datetime import date, datetime

import pytest
import pytest_asyncio
import pytz
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database.setting import Base, get_db
from src.main import app
from src.models.trend import Site, Tag, TrendData, tag_trend_data

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(TEST_DB_URL, echo=True)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # 初期データを挿入
        await create_initial_data(conn)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        yield client


# 初期データを作成する関数
async def create_initial_data(conn):
    site = Site(id=uuid.uuid4(), name="Test Site", content="Test Content")
    tag1 = Tag(id=uuid.uuid4(), name="Test Tag 1")
    tag2 = Tag(id=uuid.uuid4(), name="Test Tag 2")
    await conn.execute(Site.__table__.insert().values(id=site.id, name=site.name, content=site.content))
    await conn.execute(Tag.__table__.insert().values(id=tag1.id, name=tag1.name))
    await conn.execute(Tag.__table__.insert().values(id=tag2.id, name=tag2.name))
    # TrendDataの初期データを挿入
    trend_data = TrendData(
        id=uuid.uuid4(),
        site_id=site.id,
        title="Test TrendData",
        category="Test Category",
        published_at=datetime(2022, 1, 1, tzinfo=pytz.timezone("Asia/Tokyo")),
        url="https://example.com",
        embed_html="<div>Test Embed</div>",
        created_at=datetime(2022, 1, 1, tzinfo=pytz.timezone("Asia/Tokyo")),
    )
    await conn.execute(
        TrendData.__table__.insert().values(
            id=trend_data.id,
            site_id=trend_data.site_id,
            title=trend_data.title,
            category=trend_data.category,
            published_at=trend_data.published_at,
            url=trend_data.url,
            embed_html=trend_data.embed_html,
            created_at=trend_data.created_at,
        )
    )

    # 中間テーブルのデータを挿入
    await conn.execute(tag_trend_data.insert().values(tag_id=tag1.id, trend_id=trend_data.id))
    await conn.execute(tag_trend_data.insert().values(tag_id=tag2.id, trend_id=trend_data.id))

    await conn.commit()


@pytest.mark.asyncio
async def test_list_trend(async_client):
    filter_date = date(2022, 1, 1)
    response = await async_client.get(f"/trend?site=Test Site&filter_date={filter_date.isoformat()}")
    assert response.status_code == 200
    trend_data_list = response.json()
    assert len(trend_data_list) == 1
    assert trend_data_list[0]["title"] == "Test TrendData"
    assert trend_data_list[0]["site"]["name"] == "Test Site"
    assert len(trend_data_list[0]["tags"]) == 2
