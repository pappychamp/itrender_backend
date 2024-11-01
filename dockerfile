# 開発用のステージ
FROM python:3.12.5-slim-bullseye AS dev
RUN mkdir /workspace
WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src /workspace/src
COPY tests /workspace/tests
COPY setup.cfg /workspace/setup.cfg
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]

# lambda開発用のステージ
FROM public.ecr.aws/lambda/python:3.12 AS lambda

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY setup.cfg .

CMD ["src.main.handler"]