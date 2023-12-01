FROM python:3.8-slim-buster

WORKDIR /app
RUN mkdir -p /app

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN apt-get -y update && apt-get install -y gcc \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    musl-dev \
    rabbitmq-server

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN chmod +x ./bin/
