FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config && \
    apt-get clean


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY Requirements.txt .
RUN python -m pip install -r Requirements.txt


COPY . /app

EXPOSE 8000


RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
