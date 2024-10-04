import uuid
from datetime import date, datetime

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database.setting import Base, get_db
from src.main import app
from src.models.trend import Site, Tag, TrendData

TEST_DB_URL = "postgresql+asyncpg://postgres:postgres@test-db:5432/db-container"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(TEST_DB_URL, echo=False)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

    # テストテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            # 初期データを挿入
            await create_initial_data_session(session)
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        yield client


# 初期データを作成する関数
async def create_initial_data_session(session):

    site1 = Site(id=uuid.uuid4(), name="Site1", content="Test Content")
    site2 = Site(id=uuid.uuid4(), name="Site2", content="Test Content")
    tag1 = Tag(id=uuid.uuid4(), name="Tag1")
    tag2 = Tag(id=uuid.uuid4(), name="Tag2")
    tag3 = Tag(id=uuid.uuid4(), name="Tag3")
    # site1の1/2のランキング1の記事
    trend_data1 = TrendData(
        id=uuid.uuid4(),
        site_id=site1.id,
        title="1/2 TrendData1",
        ranking=1,
        category="Test Category",
        published_at=datetime(2024, 1, 2),
        url="https://example.com",
        embed_html="<div>Test Embed</div>",
        image_url="https://example-image.com",
        created_at=date(2024, 1, 2),
        tags=[tag1, tag2],
    )
    # site1の1/2のランキング2の記事
    trend_data2 = TrendData(
        id=uuid.uuid4(),
        site_id=site1.id,
        title="1/2 TrendData2",
        ranking=2,
        category="Test Category",
        published_at=datetime(2024, 1, 1),
        url="https://example.com",
        embed_html="<div>Test Embed</div>",
        image_url="https://example-image.com",
        created_at=date(2024, 1, 2),
        tags=[tag1],
    )
    # site2の1/2のランキング1の記事
    trend_data3 = TrendData(
        id=uuid.uuid4(),
        site_id=site2.id,
        title="1/2 TrendData3",
        ranking=1,
        category="Test Category",
        published_at=datetime(2024, 1, 1),
        url="https://example.com",
        embed_html="<div>Test Embed</div>",
        image_url="https://example-image.com",
        created_at=date(2024, 1, 2),
        tags=[],
    )
    # site1の1/1のランキング1の記事
    trend_data4 = TrendData(
        id=uuid.uuid4(),
        site_id=site1.id,
        title="12/31 TrendData4",
        ranking=1,
        category="Test Category",
        published_at=datetime(2023, 12, 31),
        url="https://example.com",
        embed_html="<div>Test Embed</div>",
        image_url="https://example-image.com",
        created_at=date(2024, 1, 1),
        tags=[tag1, tag2, tag3],
    )
    # trend_data4が別日にもトレンドになっていた記事
    trend_data5 = TrendData(
        id=uuid.uuid4(),
        site_id=site1.id,
        title="12/31 TrendData4",
        ranking=1,
        category="Test Category",
        published_at=datetime(2023, 12, 31),
        url="https://example.com",
        embed_html="<div>Test Embed</div>",
        image_url="https://example-image.com",
        created_at=date(2023, 12, 31),
        tags=[tag1, tag2, tag3],
    )
    session.add(site1)
    session.add(site2)
    session.add(tag1)
    session.add(tag2)
    session.add(tag3)
    session.add(trend_data1)
    session.add(trend_data2)
    session.add(trend_data3)
    session.add(trend_data4)
    session.add(trend_data5)

    # コミットしてデータベースに保存
    await session.commit()
