# Torchbox.com — hosts and deployment

The VM comes preinstalled with Fabric, Heroku CLI and AWS CLI.

## Deployed environments

| Environment | Branch    | URL                                         | Heroku                        |
| ----------- | --------- | ------------------------------------------- | ----------------------------- |
| Production  | `master`  | e.g. https://torchbox.com                   | e.g. `projectname-production` |
| Staging     | `staging` | e.g. https://torchbox-staging.herokuapp.com | e.g. `projectname-staging`    |

## Login to Heroku

Please log in to Heroku before executing any commands for servers hosted there.

## Connect to the shell

To open the shell of the servers.

```bash
fab staging-shell
fab production-shell
```

## Scheduled tasks

When you set up a server you should make sure the following scheduled tasks are set.

- `django-admin publish_scheduled_pages` - every 10 minutes or more often. This is necessary to make publishing scheduled pages work.
- `django-admin clearsessions` - once a day (not necessary, but useful).
- `django-admin update_index` - once a day (not necessary, but useful to make sure the search index stays intact).

## Deployment

To deploy, merge your feature branch to `master` or `staging` branch. Once CI pipelines have passed, it will be deployed to the respective Heroku site automatically.

This is done via [Heroku Github integration](https://devcenter.heroku.com/articles/github-integration). You can view the progress of the deployment by logging into Heroku, navigating to the app's dashboard and checking the "Activity" section.
