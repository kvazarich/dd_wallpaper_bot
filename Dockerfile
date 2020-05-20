FROM python:3.8.1-alpine

RUN apk add g++ python-dev libffi-dev openssl-dev jpeg-dev zlib-dev

COPY requirements.txt /bot/

COPY ./bot/ /bot/

WORKDIR /bot

RUN pip3 install --upgrade pip

RUN pip3 install --ignore-installed -r requirements.txt

RUN python3 run.py
