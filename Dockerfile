FROM heroku/heroku:22

WORKDIR /app
COPY pyproject.toml requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY src .
CMD gunicorn config.wsgi:application
