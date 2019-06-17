FROM python:3.6-alpine
ENV PYTHONUNBUFFERED=1

RUN mkdir /var/andrzej
WORKDIR /var/andrzej


RUN apk add --update --no-cache --virtual .build-deps \
    build-base \
    linux-headers \
    gcc \
    libffi-dev \
    g++ \
    libxslt-dev

COPY . .
RUN pip install -r /var/andrzej/requirements.txt
