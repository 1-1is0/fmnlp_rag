# syntax = docker/dockerfile:1
FROM python:3.11 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN --network=host <<eot
    apt-get update
    apt-get install -y netcat-traditional curl ffmpeg libsm6 libxext6
    pip install -U pip
eot


WORKDIR /app
COPY ./requirements.txt .
RUN --network=host pip install -r requirements.txt


