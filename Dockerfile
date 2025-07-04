FROM python:3.10.9-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf/var/lib/apt/list/*

COPY requirements.txt/app/

RUN pip install -no-cache-dir -r requirements.txt

COPY ./app/

RUN python manage.py collectstatic -noinput

EXPOSE 8000

ENTRYPOINT["gunicorn", "Resume-builder.wsgi", "-b", "0.0.0.0:8000"]