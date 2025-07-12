FROM python:3.10.9-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/list/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_EMAIL
ARG DJANGO_SUPERUSER_PASSWORD

ENV DJANGO_SUPERUSER_USERNAME = ${DJANGO_SUPERUSER_USERNAME}
ENV DJANGO_SUPERUSER_EMAIL = ${DJANGO_SUPERUSER_EMAIL}
ENV DJANGO_SUPERUSER_PASSWORD = ${DJANGO_SUPERUSER_PASSWORD}

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh", "gunicorn", "Resume.wsgi", "-b", "0.0.0.0:8000" ]
