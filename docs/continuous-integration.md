# Torchbox.com — Continuous Integration

## Code styleguide

This project’s code formatting is enforced with [Prettier](https://prettier.io/) for supported languages, [black](https://github.com/psf/black), [flake8](https://github.com/pycqa/flake8), and [isort](https://github.com/PyCQA/isort) for Python. Make sure to have all integrated with your editor to auto-format when saving files, or to manually run them before committing (`npm run format` for Prettier).

## Automatic linting locally

You can also run the linting tests automatically before committing. This is optional. It uses pre-commit, which is installed by default in the docker container, and a .pre-commit-config.yml file is included for the project.

To use when making commits on your host machine you must install pre-commit, either create a virtualenv to use with the project or to install globally see instructions at (https://pre-commit.com/#install).

Pre-commit will not run by default. To set it up, run `pre-commit install` inside the Docker container, or on the host if you have installed pre-commit there.

You can also manually run pre-commit without using a git hook by running:

```bash
$ pre-commit run --all-files
```

The `detect-secrets` pre-commit hook requires a baseline secrets file to be included. If you need to, you can update this file, e.g. when adding dummy secrets for unit tests:

```bash
$ detect-secrets scan > .secrets.baseline
```

## Automatic checks on Github

When commits are pushed to Github, CI pipelines including tests, and linting checks are run. This is configured here: https://github.com/torchbox/wagtail-torchbox/blob/master/.github/workflows/test.yml
