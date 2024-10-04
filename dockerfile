FROM python:3.12.5-slim-bullseye AS base

RUN mkdir /workspace
WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src /workspace/src
COPY tests /workspace/tests
COPY setup.cfg /workspace/setup.cfg

# 開発用のステージ
FROM base AS dev
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


# 本番
# FROM python:3.12.3-alpine3.20
# RUN mkdir /src
# WORKDIR /src
# COPY requirements.txt .
# COPY src/ .

# RUN pip install -r requirements.txt