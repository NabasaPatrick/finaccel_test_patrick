# Dockerfile

FROM python:3.8

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src /code/src
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini
