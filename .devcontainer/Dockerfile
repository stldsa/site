FROM mcr.microsoft.com/vscode/devcontainers/python:3.11-bullseye

ENV DJANGO_SUPERUSER_USERNAME=admin@example.com
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=stldsa
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pipx install poetry 
COPY pyproject.toml poetry.lock .
RUN poetry install
COPY .venv .venv