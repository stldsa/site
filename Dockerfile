# The base image we want to inherit from
FROM nikolaik/python-nodejs:latest

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.0.5 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    DOCKER_SETTINGS_FILE='config.settings.docker'

# System deps:
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
    # && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    # && apt-get install -y nodejs \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* 
# && pip install "poetry==$POETRY_VERSION" && poetry --version \

# set work directory
WORKDIR /code
COPY . .

# COPY . .
# Install dependencies:
RUN npm install
RUN poetry install
# copy project
CMD ["python", "manage.py", "runserver"]