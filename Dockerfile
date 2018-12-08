FROM jfloff/alpine-python

ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /

RUN pip install --upgrade pip

RUN pip install pipenv && pipenv install --system

RUN mkdir -p /apicurrency
COPY . /apicurrency
WORKDIR /apicurrency
