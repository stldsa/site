# The base image we want to inherit from
FROM python:3.9.1 AS development_build

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
    POETRY_CACHE_DIR='/var/cache/pypoetry'

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
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /code
COPY pyproject.toml poetry.lock

COPY . .
# Install dependencies:
RUN poetry install
# copy project
CMD ["python", "manage.py", "runserver"]