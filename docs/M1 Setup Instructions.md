# M1 Mac Setup Instructions

## Required File Changes

Update your redis version from 3 to 6 in `docker-compose.yml`

```yaml
---
redis:
  image: redis:6
```

In `Dockerfile.utils`, replace the Heroku installation command beneath `# Install Heroku CLI` with

```bash
# Install Heroku CLI
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs
RUN curl -s https://cli-assets.heroku.com/install.sh | sed 's/arm\*/aarch\*/g' | sh
```

## Preliminary Setup

Ask in the Heroku channel for appropriate permissions:
`heroku access:add <your email address> --app torchbox-staging`

Make sure you've updated Heroku to the latest version (with `heroku update`) or you will be denied access.

## Docker Setup

### Resolving Older Issues

If you have issues related to working on the project previously, consider running
`fab destory`
to get rid of all old containers and databases, starting the build afresh.

`fab stop` will switch off the containers without harming their data, ready for future reuse.

Restart docker desktop if old docker instances don't want to quit.

### Starting Development

Run `fab build` to make the containers.

Run `fab heroku-login` with your Heroku API key as your password. You can find this in your heroku account details page.
Run `fab pull-staging-data` to get the local environment ready for FE development.
You can also pull images with `fab pull-staging-images`, note this is a lot of data.

Run `fab start` to activate the containers,
Then `fab sh` to open the container shell.

Within the shell, run
`./manage.py createsuperuser` (Enter username, email and password)
`./manage.py createcachetable` (This should output nothing on success)
`./manage.py runserver 0.0.0.0:8000` (Brings the site online)

The site should now be accessible at [http://localhost:8000/](http://localhost:8000).

### Local Frontend Development

To automatically have CSS, JS and other changes compile and refresh in the browser during local development, you'll have to run the frontend build tools.

Open a new terminal window while keeping the server running in the background, and run the following commands.

`fnm use` (or `nvm use` if you haven't installed `fnm` yet. Note that `fnm` is far faster.)
`npm install`
`npm start`

The site should now be accessible with livereload at [http://localhost:3000](http://localhost:3000).
