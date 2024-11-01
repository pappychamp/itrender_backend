import pytest


@pytest.mark.asyncio
async def test_list_latest_trend(async_client):

    response = await async_client.get("/api/trend")
    assert len(response.json()) == 1  # 最新の情報だけ取得しているか
    assert len(response.json()["2024-01-02"]) == 2  # サイトの数だけ情報を取得しているか
    assert len(response.json()["2024-01-02"]["Site1"]) == 2  # サイトのランキング分だけ取得しているか
    assert len(response.json()["2024-01-02"]["Site2"]) == 1  # サイトのランキング分だけ取得しているか


@pytest.mark.asyncio
async def test_list_site_trend(async_client):
    mock_site_name = "Site1"
    mock_filter_date = "2024-01-02"
    response = await async_client.get(f"/api/trend/{mock_site_name}", params={"filter_date": mock_filter_date})
    assert len(response.json()) == 2  # site_nameのfilter_dateの情報だけ取得しているか


@pytest.mark.asyncio
async def test_search_words_trend(async_client):
    mock_params = {"q": ["tag1"], "size": 30, "page": 1}
    response = await async_client.get("/api/search", params=mock_params)
    # queryにヒットした記事だけ取得されているか、trend_data4,trend_data5の記事の重複をなくしているか
    assert len(response.json()["items"]) == 3
    assert response.json()["total"] == 3
