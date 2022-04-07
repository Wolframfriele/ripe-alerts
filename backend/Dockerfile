# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get install -y whois \
    && pip install -r requirements.txt
COPY . /code/