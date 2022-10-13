FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY ["catalog", "./"]