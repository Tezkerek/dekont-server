FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

RUN pip install pipenv
RUN pipenv install
