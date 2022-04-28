FROM node:14 as frontend

# Make build & post-install scripts behave as if we were in a CI environment (e.g. for logging verbosity purposes).
ARG CI=true

# Install front-end dependencies.
COPY package.json package-lock.json .babelrc.js webpack.config.js ./
RUN npm ci --no-optional --no-audit --progress=false

# Compile static files
COPY ./tbx/static_src/ ./tbx/static_src/
RUN npm run build:prod


# We use Debian images because they are considered more stable than the alpine
# ones becase they use a different C compiler. Debian images also come with
# all useful packages required for image manipulation out of the box. They
# however weight a lot, approx. up to 1.5GiB per built image.
FROM python:3.8-buster as backend

ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.1.13

RUN useradd tbx

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku or Dokku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PATH - Make sure that Poetry is on the PATH
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.8/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.8/using/cmdline.html#cmdoption-u
#  * PYTHONPATH - enables use of django-admin command.
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used. Please match with EXPOSE so it works on Dokku.
#    Heroku will ignore EXPOSE and only set PORT variable. PORT variable is
#    read/used by Gunicorn.
#  * WEB_CONCURRENCY - number of workers used by Gunicorn. The variable is
#    read by Gunicorn.
#  * GUNICORN_CMD_ARGS - additional arguments to be passed to Gunicorn. This
#    variable is read by Gunicorn
ENV PATH=$PATH:${POETRY_HOME}/bin \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=tbx.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="-c gunicorn-conf.py --max-requests 1200 --access-logfile - --timeout 25"

ARG BUILD_ENV

# Port exposed by this container. Should default to the port used by your WSGI
# server (Gunicorn). This is read by Dokku only. Heroku will ignore this.
EXPOSE 8000

# Install poetry using the installer (keeps Poetry's dependencies isolated from the app's)
RUN wget https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py && \
    echo "eedf0fe5a31e5bb899efa581cbe4df59af02ea5f get-poetry.py" | sha1sum -c - && \
    python get-poetry.py && \
    rm get-poetry.py && \
    poetry config virtualenvs.create false

# Install your app's Python requirements.
COPY --chown=tbx pyproject.toml poetry.lock ./
RUN if [ "$BUILD_ENV" = "dev" ]; then poetry install --extras gunicorn; else poetry install --no-dev --extras gunicorn; fi

COPY --chown=tbx --from=frontend ./tbx/static_compiled ./tbx/static_compiled

# Copy application code.
COPY --chown=tbx . .

# Collect static. This command will move static files from application
# directories and "static_compiled" folder to the main static directory that
# will be served by the WSGI server.
RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
USER tbx

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn tbx.wsgi:application
