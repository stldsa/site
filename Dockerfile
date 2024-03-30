FROM heroku/heroku:22

WORKDIR /app
COPY pyproject.toml requirements.lock ./
ENV PYTHONDONTWRITEBYTECODE=1
RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash && rye sync --no-dev
COPY src .
CMD gunicorn config.wsgi:application
