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
RUN poetry export --dev -f requirements.txt -o requirements.txt

RUN python -m venv /opt/venv
RUN pip install --no-cache-dir -r requirements.txt

FROM node:16-alpine as node-base
WORKDIR /opt
COPY package.json ./
RUN npm install .

FROM py-base as development

ENV DJANGO_SUPERUSER_EMAIL="admin@example.com" \
    DJANGO_SUPERUSER_PASSWORD="password" \
    DJANGO_CONFIGURATION=Docker \
    DJANGO_SETTINGS_MODULE='config.settings'

COPY --from=node-base /opt/node_modules /opt/node_modules
COPY --from=base /opt/venv /opt/venv

WORKDIR /app

CMD ["bash", "/app/init_db.sh"]