FROM mcr.microsoft.com/vscode/devcontainers/python:3.11-bullseye
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONBUFFERED=1 

WORKDIR /workspace

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SUPERUSER_USERNAME=admin@example.com \
    DJANGO_SUPERUSER_EMAIL=admin@example.com \
    DJANGO_SUPERUSER_PASSWORD=stldsa \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    DEBUG=True

RUN pipx install poetry 
COPY pyproject.toml poetry.lock .

RUN --mount=type=cache,target=/home/.cache/pypoetry/cache \
    --mount=type=cache,target=/home/.cache/pypoetry/artifacts \
    poetry install --no-root


