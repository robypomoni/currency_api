FROM jfloff/alpine-python

ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /

RUN pip install --upgrade pip

RUN pip install pipenv && pipenv install --system

RUN mkdir -p /app_data
COPY . /app_data
WORKDIR /app_data
