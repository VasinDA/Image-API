FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . /app
RUN pip install -r requirements.txt
