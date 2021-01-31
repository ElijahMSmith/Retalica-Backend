FROM python:3.8.2-slim

ENV PYTHONUNBUFFERED 1

RUN pip install django
RUN pip install praw
RUN pip install djangorestframework

WORKDIR /RetalicaBackend

COPY . /RetalicaBackend

RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:$PORT