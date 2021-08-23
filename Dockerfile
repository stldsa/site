# The base image we want to inherit from
FROM nikolaik/python-nodejs:python3.9-nodejs16


ENV DJANGO_CONFIGURATION=Docker \
    DJANGO_SETTINGS_MODULE='config.settings' \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
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
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY . .

RUN npm install
RUN poetry install

CMD ["python", "manage.py", "runserver"]