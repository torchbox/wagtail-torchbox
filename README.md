# Torchbox.com on Wagtail

[![Build Status](https://travis-ci.org/torchbox/wagtail-torchbox.svg?branch=master)](https://travis-ci.org/torchbox/wagtail-torchbox)

This is the main Torchbox.com website. The careers section of this site can be found at [torchbox/careers](https://github.com/torchbox/careers).

# Setting up a local build

This repository includes `docker-compose` configuration for running the project in local Docker containers,
and a fabfile for provisioning and managing this.

There are a number of other commands to help with development using the fabric script. To see them all, run:

```bash
fab -l
```

## Dependencies

The following are required to run the local environment. The minimum versions specified are confirmed to be working:
if you have older versions already installed they _may_ work, but are not guaranteed to do so.

- [Docker](https://www.docker.com/), version 19.0.0 or up
  - [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) installer
  - [Docker Engine for Linux](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc&operating_system=linux) installers
- [Docker Compose](https://docs.docker.com/compose/), version 1.24.0 or up
  - [Install instructions](https://docs.docker.com/compose/install/) (Linux-only: Compose is already installed for Mac users as part of Docker Desktop.)
- [Fabric](https://www.fabfile.org/), version 2.4.0 or up
  - [Install instructions](https://www.fabfile.org/installing.html)
- Python, version 3.6.9 or up

Note that on Mac OS, if you have an older version of fabric installed, you may need to uninstall the old one and then install the new version with pip3:

```bash
pip uninstall fabric
pip3 install fabric
```

You can manage different python versions by setting up `pyenv`: https://realpython.com/intro-to-pyenv/

Additionally, for interacting with production / staging environments, you'll need:

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

## Running the local build for the first time

If you are using Docker Desktop, ensure the Resources:File Sharing settings allow the cloned directory to be mounted in the web container (avoiding `mounting` OCI runtime failures at the end of the build step).

Starting a local build can be done by running:

```bash
git clone git@github.com:torchbox/wagtail-torchbox.git
cd wagtail-torchbox
fab build
fab migrate
fab start
```

This will start the containers in the background, but not Django. To do this, connect to the web container with `fab sh` and run `honcho start` to start both Django and the Webpack dev server in the foreground.

Then, connect to the running container again (`fab sh`) and:

```bash
dj createcachetable
dj createsuperuser
```

The site should be available on the host machine at: http://127.0.0.1:8000/

If you only wish to run the frontend or backend tooling, the commands `honcho` runs are in `docker/Procfile`.

Upon first starting the container, the static files may not exist, or may be out of date. To resolve this, simply run `npm run build`.

### Frontend tooling

Here are the common commands:

```bash
# Install front-end dependencies.
npm install
# Start the Webpack build in watch mode, without live-reload.
npm run start
# Start the Webpack server build on port 3000 only with live-reload.
npm run build
# Do a one-off Webpack production build.
npm run build:prod
```

There are two ways to run the frontend tooling:

- In Docker. This is the default, most portable and secure, but much slower on macOS.
- Or run npm commands from a terminal on your local machine. Create a `.env` file in the project root (see `.env.example`) with `FRONTEND=local`. `fab start` will no longer start a `frontend` container. Now, when running `fab start`, Docker won't attempt to bind to the ports needed for the frontend dev server, meaning they can be run locally. All the tooling still remains available in the container.

## Installing python packages

Python packages can be installed using `poetry` in the web container:

```
fab sh
poetry add wagtail-guide
```

To reset installed dependencies back to how they are in the `poetry.lock` file:

```
fab sh
poetry install --no-root
```

## Deployments

To deploy push branch to heroku manually:

### Staging

Add remote on your local repo:
`heroku git:remote -a torchbox-staging`

Rename the remote to avoid confusion with prod
`git remote rename heroku heroku-staging`

Push branch to heroku:
`git push heroku-staging staging:main`

### Production

Add remote on your local repo:
`heroku git:remote -a cms-torchbox-com`

Rename the remote to avoid confusion with staging
`git remote rename heroku heroku-prod`

Push branch to heroku:
`git push heroku-prod master:main`
