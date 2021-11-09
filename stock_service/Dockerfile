FROM python:3.7-alpine
MAINTAINER matheustguimaraes

ENV PYTHONUNBUFFERED 1

RUN mkdir /stock

WORKDIR /stock
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
