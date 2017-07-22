FROM python:2.7-alpine

WORKDIR /api
ADD ./src/requirements.txt /api
RUN pip install -r requirements.txt
