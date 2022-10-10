# The base image we want to inherit from
FROM python:3.10.7-slim-buster as py-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM py-base as base

RUN apt-get update && apt-get install -y --no-install-recommends\
    build-essential \
    curl \
    libpq-dev \
    python3-dev \
    git

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

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

WORKDIR $PYSETUP_PATH

COPY --from=base $POETRY_HOME $POETRY_HOME
COPY --from=base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=node-base /opt/node_modules /opt/node_modules
COPY --from=sass /dart-sass /opt/sass

RUN ls $PYSETUP_PATH
RUN ls $POETRY_HOME
RUN poetry install

WORKDIR /app


# CMD ["bash", "/app/init_db.sh"]