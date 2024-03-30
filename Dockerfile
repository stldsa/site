FROM heroku/heroku:22

WORKDIR /app
COPY pyproject.toml requirements.lock ./
ENV PYTHONDONTWRITEBYTECODE=1 \
    RYE_HOME=/usr/local/lib/rye
RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash && /usr/local/lib/rye/shims/rye sync --no-dev
COPY src .
CMD /usr/local/lib/rye/shims/rye gunicorn config.wsgi:application
