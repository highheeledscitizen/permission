FROM python:3.12-slim


RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /tsy_project

COPY ./hw7 /tsy_project/hw7

RUN pip install --no-cache-dir -r /tsy_project/hw7/requirements.txt

WORKDIR /tsy_project/hw7

EXPOSE 8000
