FROM mcr.microsoft.com/vscode/devcontainers/python:3.11-bullseye

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

ENV DJANGO_SUPERUSER_USERNAME=admin@example.com
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=stldsa
ENV POETRY_VIRTUALENVS_IN_PROJECT=true