FROM python:latest

ADD scheduler/requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

EXPOSE 18888

RUN adduser --disabled-password --gecos '' app