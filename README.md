# 概要
アプリのバックエンド

# テスト方法
```bash
docker compose build 
docker compose up -d
docker container exec test-backend pytest --junitxml=pytest.xml --cov-report=term-missing --cov=src tests/ | tee pytest-coverage.txt
```