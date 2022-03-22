# Torchbox.com on Wagtail

[![Build Status](https://travis-ci.org/torchbox/wagtail-torchbox.svg?branch=master)](https://travis-ci.org/torchbox/wagtail-torchbox)

This is the main Torchbox.com website. The careers section of this site can be found at [torchbox/careers](https://github.com/torchbox/careers).

# Project Setup

This repository includes `docker-compose` configuration for running the project in local Docker containers,
and a fabfile for provisioning and managing this.

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

## Required Permissions

Ask in the Heroku channel for staging access permissions:
`heroku access:add <your email address> --app torchbox-staging`

Make sure you've updated Heroku to the latest version (with `heroku update`) or you will be denied access.

Ask another developer for permissions to clone and make merge requests to the [GitHub repository](https://github.com/torchbox/wagtail-torchbox).

## Running the Local Build for the First Time

If you are using Docker Desktop, ensure the Resources:File Sharing settings allow the cloned directory to be mounted in the web container (avoiding `mounting` OCI runtime failures at the end of the build step).

Starting a local build can be done by running:

```bash
git clone https://github.com/torchbox/wagtail-torchbox.git
cd tbx
fab build
```

Then, to pull staging data from Heroku,

```bash
fab heroku-login
```

Use your Heroku API key as your password. You can find this in your heroku account details page.

```bash
fab pull-staging-data
```

You can also pull images from the site with `fab pull-staging-images`, note this is a lot of data.

Now run

```bash
fab start
fab sh
```

Then within the SSH session:

```bash
./manage.py migrate
./manage.py createcachetable
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```

The site should be available at: [http://localhost:8000/](http://localhost:8000).

## Frontend Development

To automatically have CSS, JS and other file changes compile and refresh in the browser during local development, you'll have to run the frontend build tools.

There are 2 ways to run the frontend tooling:

### Locally

Open a new terminal window while keeping the server running in the background, and run the following commands.

```bash
nvm use
npm install
npm start
```

The site should now be accessible with livereload at [http://localhost:3000](http://localhost:3000).

Note that `fnm` is a faster version of `nvm` which behaves in the same way. [See the repository for installation instructions](https://github.com/Schniz/fnm).

### Within the Frontend Docker Container

After starting the containers as above and running `./manage.py runserver 0:8000`, open a new
terminal session and run `fab npm start`.

The site should now be accessible with livereload at [http://localhost:3000](http://localhost:3000).

## Front-end assets

Frontend npm packages can be installed locally with npm, then added to the frontend container with fabric like so:

```bash
npm install promise
fab npm install
```

## Installing Python Packages

Python packages can be installed using poetry in the web container:

```
fab sh-root
poetry install wagtail-guide
```

## Deployments

Merges to `master` and `staging` will automatically trigger a deployment to the production and staging sites, respectively.

## How To Reset the Docker Containers

If you have issues related to working on the project previously, consider running
`fab destroy`
to get rid of all old containers and databases, starting the build afresh.

`fab stop` will switch off the containers without harming their data, ready for future reuse.

Restart docker desktop if old docker instances don't want to quit.

## Other Fab Commands

There are a number of other commands to help with development using the fabric script. To see them all, run:

```bash
fab -l
```
