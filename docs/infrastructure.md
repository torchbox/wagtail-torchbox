Torchbox.com Infrastructure

## Database

Postgres

#### Pulling data

To populate your local database with the content of staging/production:

```bash
fab pull-staging-data
fab pull-production-data
```

To get images for a build, the following commands will fetch original images only, with no documents, leaving your local build to create image renditions when needed:

```sh
fab pull-staging-images
fab pull-production-images
```

If you do need everything, fetch all media:

```bash
fab pull-staging-media
fab pull-production-media
```

## Cache

TODO:

What cache backend is used? What is it used for?

What front-end cache is there on production? How is it configured?

## File storage

This site uses AWS S3 for storage.

## DNS

## TLS/SSL/HTTPS

## Resetting the Staging site

Steps for resetting the `staging` git branch, and deploying it with a clone of the production site database.

### Pre-flight checks

1. Is this okay with the client, and other developers?
1. Is there any test content on staging that may need to be recreated, or be a reason to delay?
1. What branches are currently merged to staging?

   ```bash
   $ git branch -a --merged origin/staging > branches_on_staging.txt
   $ git branch -a --merged origin/master > branches_on_master.txt
   $ diff branches_on_{master,staging}.txt
   ```

   Take note if any of the above are stale, not needing to be recreated.

1. Are there any user accounts on staging only, which will need to be recreated? Check with the client, and record them.
1. Take a backup of staging
   ```bash
   $ heroku pg:backups:capture -a projectname-staging
   ```

### Git

1. Reset the staging branch
   ```bash
   $ git checkout staging && git fetch && git reset --hard origin/master && git push --force
   ```
1. Tell your colleagues
   > @here I have reset the staging branch. Please delete your local staging branches
   >
   > ```
   > $ git branch -D staging
   > ```
   >
   > to avoid accidentally merging in the old version
1. Force-push to Heroku, otherwise CI will later fail `$ git push --force heroku-staging master` (this will trigger a deployment, bear in mind that there may be incompatibilities between the old staging database and the new code from master; this will be resolved in the Database step below)
1. Merge in the relevant branches
   ```bash
   $ git merge --no-ff origin/feature/123-extra-spangles
   ```
1. Check for any newly necessary merge migrations `$ ./manage.py makemigrations --check`

### Database

This site uses flightpath to manage staging reset. This is implemented as [Copy prod to staging](https://github.com/torchbox/wagtail-torchbox/actions/workflows/flightpath.yml) Github Actions.

To run, go the [Github Actions page](https://github.com/torchbox/wagtail-torchbox/actions/workflows/flightpath.yml), click on 'Rub workflow', and select `master`.

### Media

This will be copied by Flightpath.

### Cleanup

1. Check the staging site loads
1. Update the Wagtail Site records, as the database will contain the production URLs
1. Check CI is working

### Comms

1. Inform the client of the changes, e.g.
   > All user accounts have been copied across, so your old staging password will no longer work. Log in with your production password (and then change it), or use the 'forgot password' feature.
   > Any test content has been reset. This is probably the biggest inconvenience. Sorry.
   > I have deleted the personally-identifying data from form submissions **and anywhere else relevant**. If there's any more on production (there shouldn't be) then please let me know and I'll remove it from staging.
