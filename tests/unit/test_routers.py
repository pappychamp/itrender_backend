from datetime import date
from unittest.mock import ANY

import pytest

# list_latest_trendのテスト


@pytest.mark.asyncio
class TestListLatestTrend:
    async def test_success(self, async_client, mocker):
        # get_latest_date のモック
        mock_latest_date = date(2024, 1, 1)
        mock_get_latest_date = mocker.patch("src.routers.trend.get_latest_date")
        mock_get_latest_date.return_value = mock_latest_date
        # get_all_site_trend_data のモック
        mock_get_all_site_trend_data = mocker.patch("src.routers.trend.get_all_site_trend_data")
        mock_get_all_site_trend_data.return_value = []

        # リクエストを実行してレスポンスを確認
        response = await async_client.get("/trend")
        mock_get_latest_date.assert_called_once()
        mock_get_all_site_trend_data.assert_called_once()
        mock_get_all_site_trend_data.assert_called_once_with(mock_latest_date, ANY)  # sessionをANYに
        assert response.status_code == 200

    async def test_failure(self, async_client, mocker):
        mock_get_latest_date = mocker.patch("src.routers.trend.get_latest_date")
        # logger.info をモック
        mock_logger = mocker.patch("src.routers.trend.logger.info")
        mock_get_latest_date.side_effect = Exception("new exception")

        mock_get_all_site_trend_data = mocker.patch("src.routers.trend.get_all_site_trend_data")
        mock_get_all_site_trend_data.return_value = []

        response = await async_client.get("/trend")
        mock_get_latest_date.assert_called_once()
        mock_get_all_site_trend_data.assert_not_called()
        assert response.status_code == 500
        # logger.info が適切に呼び出されたか確認
        mock_logger.assert_called_once()


# list_site_trendのテスト
@pytest.mark.asyncio
class TestListSiteTrend:
    async def test_success(self, async_client, mocker):
        # 引数のモック
        mock_site_name = "test"
        mock_filter_date = date(2024, 1, 1)
        # get_site_trend_data のモック
        mock_get_site_trend_data = mocker.patch("src.routers.trend.get_site_trend_data")
        mock_get_site_trend_data.return_value = []

        # リクエストを実行してレスポンスを確認
        response = await async_client.get(f"/trend/{mock_site_name}", params={"filter_date": mock_filter_date})
        mock_get_site_trend_data.assert_called_once()
        mock_get_site_trend_data.assert_called_once_with(mock_site_name, mock_filter_date, ANY)  # sessionをANYに
        assert response.status_code == 200

    async def test_failure(self, async_client, mocker):
        mock_site_name = "test"
        mock_filter_date = date(2024, 1, 1)
        # logger.info をモック
        mock_logger = mocker.patch("src.routers.trend.logger.info")

        mock_get_site_trend_data = mocker.patch("src.routers.trend.get_site_trend_data")
        mock_get_site_trend_data.side_effect = Exception("new exception")

        response = await async_client.get(f"/trend/{mock_site_name}", params={"filter_date": mock_filter_date})
        mock_get_site_trend_data.assert_called_once()
        mock_get_site_trend_data.assert_called_once_with(mock_site_name, mock_filter_date, ANY)  # sessionをANYに
        assert response.status_code == 500
        # logger.info が適切に呼び出されたか確認
        mock_logger.assert_called_once()

    async def test_missing_filter_date(self, async_client, mocker):
        mock_site_name = "test"
        # logger.error をモック
        mock_logger = mocker.patch("src.main.logger.error")

        response = await async_client.get(f"/trend/{mock_site_name}")
        assert response.status_code == 422
        # logger.error が適切に呼び出されたか確認
        mock_logger.assert_called_once()


# search_words_trendのテスト
@pytest.mark.asyncio
class TestSearchWordsTrend:
    async def test_success(self, async_client, mocker):
        # パラメーターのモック
        mock_params = {"q": ["test1", "test2"], "size": 30, "page": 2}

        # get_filter_word_trend_data のモック
        mock_get_filter_word_trend_data = mocker.patch("src.routers.trend.get_filter_word_trend_data")
        mock_get_filter_word_trend_data.return_value = []

        # リクエストを実行してレスポンスを確認
        response = await async_client.get("/search", params=mock_params)
        mock_get_filter_word_trend_data.assert_called_once()
        mock_get_filter_word_trend_data.assert_called_once_with(["test1", "test2"], ANY)  # sessionをANYに
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["total"] == 0  # データがないため、トータルは0を期待
        assert response_data["items"] == []  # 空のリストが返ってくる
        assert response_data["page"] == 2  # ページ番号
        assert response_data["size"] == 30  # ページサイズ

    async def test_default_page_size(self, async_client, mocker):
        mock_params = {"q": ["test1", "test2"]}

        mock_get_filter_word_trend_data = mocker.patch("src.routers.trend.get_filter_word_trend_data")
        mock_get_filter_word_trend_data.return_value = []

        response = await async_client.get("/search", params=mock_params)
        mock_get_filter_word_trend_data.assert_called_once()
        mock_get_filter_word_trend_data.assert_called_once_with(["test1", "test2"], ANY)  # sessionをANYに
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["total"] == 0
        assert response_data["items"] == []
        assert response_data["page"] == 1
        assert response_data["size"] == 20

    async def test_failure(self, async_client, mocker):
        mock_params = {"q": ["test1", "test2"], "size": 20, "page": 1}
        # logger.info をモック
        mock_logger = mocker.patch("src.routers.trend.logger.info")

        mock_get_filter_word_trend_data = mocker.patch("src.routers.trend.get_filter_word_trend_data")
        mock_get_filter_word_trend_data.side_effect = Exception("new exception")

        response = await async_client.get("/search", params=mock_params)
        mock_get_filter_word_trend_data.assert_called_once()
        mock_get_filter_word_trend_data.assert_called_once_with(["test1", "test2"], ANY)  # sessionをANYに
        assert response.status_code == 500
        # logger.info が適切に呼び出されたか確認
        mock_logger.assert_called_once()

    async def test_missing_query(self, async_client, mocker):
        mock_params = {"size": 20, "page": 1}
        # logger.error をモック
        mock_logger = mocker.patch("src.main.logger.error")

        response = await async_client.get("/search", params=mock_params)
        assert response.status_code == 422
        # logger.error が適切に呼び出されたか確認
        mock_logger.assert_called_once()

    async def test_query_limit_exceeded(self, async_client, mocker):
        mock_params = {"q": ["test1", "test2", "test3", "test4"], "size": 20, "page": 1}
        # logger.error をモック
        mock_logger = mocker.patch("src.main.logger.error")

        response = await async_client.get("/search", params=mock_params)
        assert response.status_code == 422
        # logger.error が適切に呼び出されたか確認
        mock_logger.assert_called_once()
