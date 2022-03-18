# Torchbox.com on Wagtail

[![Build Status](https://travis-ci.org/torchbox/wagtail-torchbox.svg?branch=master)](https://travis-ci.org/torchbox/wagtail-torchbox)

This is the main Torchbox.com website.

# Setting up a local build

This repository includes `docker-compose` configuration for running the project in local Docker containers,
and a fabfile for provisioning and managing this.

If you are an M1 mac user, you may have to make changes to the docker configuration: see the M1 Setup Instructions in the docs.

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

## Running the local build for the first time

If you are using Docker Desktop, ensure the Resources:File Sharing settings allow the cloned directory to be mounted in the web container (avoiding `mounting` OCI runtime failures at the end of the build step).

Starting a local build can be done by running:

```bash
git clone [URL TO GIT REMOTE]
cd tbx
fab build
fab start
fab sh
```

Then within the SSH session:

```bash
./manage.py migrate
./manage.py createcachetable
./manage.py createsuperuser
./manage.py runserver 0:8000

```

The site should be available on the host machine at: http://127.0.0.1:8000/

### Frontend tooling

There are 2 ways to run the frontend tooling:

#### With the frontend docker container (default)

After starting the containers as above and running `./manage.py runserver 0:8000`, in a new
terminal session run `fab npm start`. This will start the frontend container and the site will
be available on port :3000 using browsersync. E.G `localhost:3000`.

#### Locally

To run the FE tooling locally. Create a `.env` file in the project root (see .env.example) and add `FRONTEND=local`.
Running `fab start` will now run the frontend container and you can start npm locally instead

There are a number of other commands to help with development using the fabric script. To see them all, run:

```bash
fab -l
```

## Front-end assets

Frontend npm packages can be installed locally with npm, then added to the frontend container with fabric like so:

```bash
npm install promise
fab npm install
```

## Installing python packages

Python packages can be installed using poetry in the web container:

```
fab sh-root
poetry install wagtail-guide
```

### Deployments

Merges to `master` and `staging` will automatically trigger a deployment to the production and staging sites, respectively.
