# The base image we want to inherit from
FROM python:3.9 as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.8 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential 
        
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $POETRY_VIRTUALENVS_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

FROM base as base-node

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

FROM base-node as development

WORKDIR $POETRY_VIRTUALENVS_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $POETRY_VIRTUALENVS_PATH $POETRY_VIRTUALENVS_PATH

RUN poetry install

WORKDIR /app

ENV DJANGO_CONFIGURATION=Docker \
    DJANGO_SETTINGS_MODULE='config.settings'

COPY . .

RUN ln -s $VENV_PATH .venv

RUN npm install

CMD ["python", "manage.py", "runserver"]