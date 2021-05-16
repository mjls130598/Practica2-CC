FROM python:3.7-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN apk add --no-cache --update gcc g++\
    gfortran musl-dev openblas-dev lapack git
RUN pip install -r requirements.txt