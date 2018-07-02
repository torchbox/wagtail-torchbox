# Build Python app.
FROM python:2.7-stretch

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=tbx.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="--max-requests 1200 --access-logfile -"

EXPOSE 8000

# Install operating system dependencies.
RUN apt-get update -y && \
    apt-get install -y apt-transport-https rsync && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - &&\
    apt-get install -y nodejs &&\
    rm -rf /var/lib/apt/lists/*

# Install Gunicorn.
RUN pip install "gunicorn>=19.8,<19.9"

WORKDIR tbx/static_src

# Install front-end dependencies.
COPY ./tbx/static_src/package.json ./tbx/static_src/package-lock.json ./
RUN npm install

# Install Python requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Compile static files
COPY ./tbx/static_src/ ./
RUN npm run build:prod

WORKDIR /app

# Copy application code.
COPY . .

# Install assets
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
RUN useradd tbx
RUN chown -R tbx .
USER tbx

# Run application
CMD gunicorn tbx.wsgi:application
