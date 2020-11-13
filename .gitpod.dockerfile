FROM gitpod/workspace-postgres

WORKDIR /app

# Install front-end dependencies.
COPY package.json package-lock.json .babelrc.js webpack.config.js ./
RUN npm i --no-optional --no-audit --progress=false

# Compile static files
COPY ./tbx/static_src/ ./tbx/static_src/
RUN npm run build:prod

ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.1.1

ENV PATH=$PATH:${POETRY_HOME}/bin \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=tbx.settings.production \
    PORT=8000

# Install poetry using the installer (keeps Poetry's dependencies isolated from the app's)
RUN wget https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py && \
    echo "eedf0fe5a31e5bb899efa581cbe4df59af02ea5f get-poetry.py" | sha1sum -c - && \
    python get-poetry.py && \
    rm get-poetry.py && \
    poetry config virtualenvs.create false

# Install your app's Python requirements.
COPY --chown=tbx pyproject.toml poetry.lock ./
RUN poetry install
