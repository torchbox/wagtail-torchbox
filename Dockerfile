FROM node:16 as frontend

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
FROM python:3.11 as production

ARG POETRY_INSTALL_ARGS="--no-dev"

# IMPORTANT: Remember to review both of these when upgrading
ARG POETRY_VERSION=1.5.1

# Install dependencies in a virtualenv
ENV VIRTUAL_ENV=/venv

RUN useradd tbx --create-home && mkdir /app $VIRTUAL_ENV && chown -R tbx /app $VIRTUAL_ENV

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku or Dokku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PATH - Make sure that Poetry is on the PATH, along with our venv
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.9/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.9/using/cmdline.html#cmdoption-u
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used. Please match with EXPOSE so it works on Dokku.
#    Heroku will ignore EXPOSE and only set PORT variable. PORT variable is
#    read/used by Gunicorn.
#  * WEB_CONCURRENCY - number of workers used by Gunicorn. The variable is
#    read by Gunicorn.
#  * GUNICORN_CMD_ARGS - additional arguments to be passed to Gunicorn. This
#    variable is read by Gunicorn
ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    POETRY_INSTALL_ARGS=${POETRY_INSTALL_ARGS} \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=tbx.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="-c gunicorn-conf.py --max-requests 1200 --max-requests-jitter 50 --access-logfile - --timeout 25"

# Make $BUILD_ENV available at runtime
ARG BUILD_ENV
ENV BUILD_ENV=${BUILD_ENV}


# Port exposed by this container. Should default to the port used by your WSGI
# server (Gunicorn). This is read by Dokku only. Heroku will ignore this.
EXPOSE 8000

# Install poetry at the system level
RUN pip install --no-cache poetry==${POETRY_VERSION}

USER tbx

# Install your app's Python requirements.
RUN python -m venv $VIRTUAL_ENV
COPY --chown=tbx pyproject.toml poetry.lock ./
RUN pip install --no-cache --upgrade pip && poetry install ${POETRY_INSTALL_ARGS} --no-root --extras gunicorn && rm -rf $HOME/.cache

COPY --chown=tbx --from=frontend ./tbx/static_compiled ./tbx/static_compiled

# Copy application code.
COPY --chown=tbx . .

# Run poetry install again to install our project (so the the tbx package is always importable)
RUN poetry install ${POETRY_INSTALL_ARGS}

# Collect static. This command will move static files from application
# directories and "static_compiled" folder to the main static directory that
# will be served by the WSGI server.
RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

# Load shortcuts
COPY ./docker/bashrc.sh /home/tbx/.bashrc

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn tbx.wsgi:application

# These steps won't be run on production
FROM production as dev

# Swap user, so the following tasks can be run as root
USER root

# Install `psql`, useful for `manage.py dbshell`
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    postgresql-client jpegoptim pngquant gifsicle libjpeg-progs webp \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# Restore user
USER tbx

# Install nvm and node/npm
ARG NVM_VERSION=0.39.5
COPY --chown=tbx .nvmrc ./
RUN curl https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash \
    && bash --login -c "nvm install --no-progress && nvm alias default $(nvm run --silent --version)"

# Pull in the node modules for the frontend
COPY --chown=tbx --from=frontend ./node_modules ./node_modules

# do nothing forever - exec commands elsewhere
CMD tail -f /dev/null
