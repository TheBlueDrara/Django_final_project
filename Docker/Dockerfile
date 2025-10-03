FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install --no-cache-dir -r requirements.txt
COPY src/web_app/ /app
COPY config/ /app/config
CMD ["gunicorn", "mysite.wsgi:application", "-c", "config/gunicorn_conf.py"]