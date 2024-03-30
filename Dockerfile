FROM heroku/heroku:22

WORKDIR /app
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1 \
    RYE_HOME=/usr/local/lib/rye
RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash && /usr/local/lib/rye/shims/rye sync --no-dev --no-lock

CMD /usr/local/lib/rye/shims/rye run gunicorn config.wsgi:application
