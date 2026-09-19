FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv/auditflow

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev pkg-config libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements*.txt ./
RUN pip install -U pip && pip install -r requirements-dev.txt

COPY . .
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "-c", "deploy/gunicorn.conf.py"]
