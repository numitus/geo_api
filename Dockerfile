FROM python:3.11

ENV PYTHONBUFFERED 1

WORKDIR /code


RUN pip install poetry

COPY requirements.txt /code


RUN pip3 install -r requirements.txt

COPY ./backend /code/backend
COPY ./celeryapp /code/celeryapp
