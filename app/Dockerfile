FROM python:3.8.6-slim-buster

WORKDIR /app

COPY ./app /app
COPY requirements.txt requirements.txt
RUN ls -la /app/*

RUN pip install -r requirements.txt

EXPOSE 8000 5006

# RUN python download_sample_data.py

CMD gunicorn -w 4 --bind 0.0.0.0:8000 main:app
