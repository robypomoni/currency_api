FROM jfloff/alpine-python

ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /

RUN pip install --upgrade pip

RUN pip install pipenv && pipenv install --system

RUN mkdir -p /www
COPY . /www
WORKDIR /www
