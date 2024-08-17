FROM python:3.12.3-alpine3.20
RUN mkdir /src
WORKDIR /src
COPY requirements.txt .
COPY src/ .

RUN pip install -r requirements.txt 