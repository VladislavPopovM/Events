FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /main/

WORKDIR /main/

RUN pip install -r requirements.txt