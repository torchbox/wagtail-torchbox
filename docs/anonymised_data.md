# Torchbox.com — Anonymising data

When pulling data from any hosted instance, take a cautious approach about whether you need full details of potentially personally-identifying, confidential or sensitive data.

## General principles:

- pull data from staging rather than production servers, if this is good enough for your needs
- if it is necessary to pull data from production, e.g. for troubleshooting, consider whether anonymising personal data is possible and compatible with your needs
- if it is necessary to pull non-anonymised data from production, consider destroying this copy of the data as soon as you no longer need it

In more sensitive cases, consider a data protection policy to prevent access to production data except for authorised users.

## Anonymise

`django-birdbath` provides a management command (`run_birdbath`) that will anonymise the database.

As and when models/fields are added that may be populated with sensitive data (such as email addresses) a processor should be added to ensure that the data can be anonymised or deleted when it is copied from the production environment.

For full documentation see https://git.torchbox.com/internal/django-birdbath/-/blob/master/README.md.

If data directly from **production** is required, then `run_birdbath` command should be run immediately after download.
