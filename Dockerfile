# The base image we want to inherit from
FROM python:3.9.6-slim-buster as py-base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="/opt/venv/bin:$PATH"

FROM py-base as base

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential \
    gcc 

RUN pip install poetry==1.1.8

WORKDIR /opt
COPY poetry.lock pyproject.toml ./
RUN poetry export --dev --without-hashes -f requirements.txt -o requirements.txt

RUN python -m venv /opt/venv
RUN pip install --no-cache-dir -r requirements.txt

FROM node:16-alpine as node-base

WORKDIR /opt
COPY package.json ./
RUN npm install .

FROM alpine:3.14.1 as sass
RUN wget -qO- \
https://github.com/sass/dart-sass/releases/download/1.38.1/dart-sass-1.38.1-linux-x64.tar.gz | \
tar xvz

FROM py-base as development

ENV DJANGO_SUPERUSER_EMAIL="admin@example.com" \
    DJANGO_SUPERUSER_PASSWORD="stldsa" \
    DJANGO_CONFIGURATION=Docker \
    DJANGO_SETTINGS_MODULE='config.settings' \
    PATH="/opt/sass:$PATH"

COPY --from=node-base /opt/node_modules /opt/node_modules
COPY --from=base /opt/venv /opt/venv
COPY --from=sass /dart-sass /opt/sass

COPY . /app/

WORKDIR /app

# CMD ["bash", "/app/init_db.sh"]