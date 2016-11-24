from __future__ import with_statement

import os
import uuid

from fabric.api import env, get, local, puts, roles, run
from fabric.contrib.console import confirm

STAGING_HOST = 'by-staging-1.torchbox.com'
PRODUCTION_HOST_1 = 'web-1-a.rslon.torchbox.net'
PRODUCTION_HOST_2 = 'web-1-b.rslon.torchbox.net'

env.roledefs = {
    'staging': ['tbxwagtail@{}'.format(STAGING_HOST)],
    'live': ['tbxwagtail@{}'.format(PRODUCTION_HOST_1),
             'tbxwagtail@{}'.format(PRODUCTION_HOST_2)],
}
env.always_use_pty = False

PROJECT_NAME = "wagtail-torchbox"
LOCAL_DB_NAME = "torchbox"
LOCAL_DUMP_PATH = "/tmp/"
LOCAL_MEDIA_DIR = "/vagrant/media"

REMOTE_DB_NAME = '$CFG_DB_NAME'
REMOTE_DB_USERNAME = '$CFG_DB_USER'
ENV_PROJECT_PATH_VARIABLE = 'D'
REMOTE_PROJECT_PATH = '$D/'
REMOTE_DUMP_PATH = '{}tmp/'.format(REMOTE_PROJECT_PATH)
ENV_MEDIA_DIR_VARIABLE = 'CFG_MEDIA_DIR'
REMOTE_MEDIA_DIR = '$CFG_MEDIA_DIR'


def _fetch_remote_variable(input_string):
    """ Runs `echo $SOMEVAR`, with no terminal assigned, so that the server
    doesn't add extra bumf to stdout.
    """
    return run('echo {}'.format(input_string), pty=False)


def _deploy():

    if env['host'] == STAGING_HOST:
        branch = 'staging'
    else:
        branch = 'master'

    current_branch = run('git symbolic-ref --short HEAD')
    if current_branch != branch:
        puts("Remote server is on {}. You are trying to deploy {}. This "
             "script does not support branch switching.".format(current_branch, branch))
        return
    run('git pull')
    run('pip install -r requirements.txt')
    run('dj migrate --noinput')
    run('dj collectstatic --noinput')
    run('restart')
    run('python -m whitenoise.compress $CFG_STATIC_DIR')


def _pull_data():
    if env['host'] == PRODUCTION_HOST_2:
        # No need to pull data twice
        return

    filename = "{}-{}.sql".format(PROJECT_NAME, uuid.uuid4())
    local_path = "{}{}".format(LOCAL_DUMP_PATH, filename)
    remote_path = "{}{}".format(REMOTE_DUMP_PATH, filename)
    local_db_backup_path = "{}vagrant-{}-{}.sql".format(LOCAL_DUMP_PATH, LOCAL_DB_NAME, uuid.uuid4())
    non_env_remote_path = _fetch_remote_variable(remote_path)

    run('pg_dump -U{} -xOf {} {}'.format(REMOTE_DB_USERNAME, remote_path, REMOTE_DB_NAME))
    run('gzip {}'.format(remote_path))
    get("{}.gz".format(non_env_remote_path), "{}.gz".format(local_path))
    run('rm {}.gz'.format(remote_path))

    local('pg_dump -xOf {} {}'.format(local_db_backup_path, LOCAL_DB_NAME))
    puts('Previous local database backed up to {}'.format(local_db_backup_path))

    local('dropdb {}'.format(LOCAL_DB_NAME))
    local('createdb {}'.format(LOCAL_DB_NAME))
    local('gunzip {}.gz'.format(local_path))
    local('psql {} -f {}'.format(LOCAL_DB_NAME, local_path))
    local('rm {}'.format(local_path))


def _pull_live_data_from_staging():
    """ Marginally different from _pull_data; uses remote variables for local
    paths etc., as the local environment is presumed to be staging server.
    """
    if env['host'] == PRODUCTION_HOST_2:
        # No need to pull data twice
        return

    filename = "{}-{}.sql".format(PROJECT_NAME, uuid.uuid4())
    project_path = os.getenv(ENV_PROJECT_PATH_VARIABLE)
    universal_path = "{}/tmp/{}".format(project_path, filename)
    staging_db_backup_path = "{}staging-{}-{}.sql".format(REMOTE_DUMP_PATH, REMOTE_DB_NAME, uuid.uuid4())

    run('pg_dump -U{} -xOf {} {}'.format(REMOTE_DB_USERNAME, universal_path, REMOTE_DB_NAME))
    run('gzip {}'.format(universal_path))
    local('echo {}'.format(universal_path))
    local('echo {}'.format(os.getenv(universal_path)))
    get("{}.gz".format(universal_path), "{}.gz".format(universal_path))
    run('rm {}.gz'.format(universal_path))

    local('pg_dump -xOf {} {}'.format(staging_db_backup_path, REMOTE_DB_NAME))
    puts('Previous local database backed up to {}'.format(staging_db_backup_path))

    local("psql -c 'DROP SCHEMA public CASCADE;'")
    local("psql -c 'CREATE SCHEMA public;'")
    local('gunzip {}.gz'.format(universal_path))
    local('psql {} -f {}'.format(REMOTE_DB_NAME, universal_path))
    local('rm {}'.format(universal_path))


def _pull_media():
    if env['host'] == PRODUCTION_HOST_2:
        # No need to pull media twice
        return
    non_env_remote_media_path = _fetch_remote_variable(REMOTE_MEDIA_DIR)
    local('rm -rf media.old')
    local('cp -r {} {}.old || true'.format(LOCAL_MEDIA_DIR, LOCAL_MEDIA_DIR))

    local('rsync -avz %s:%s/ /vagrant/media/' % (env['host_string'], non_env_remote_media_path))


def _pull_live_media_from_staging():
    """ Marginally different from _pull_media; uses remote variables for local
    paths etc., as the local environment is presumed to be staging server.
    """
    if env['host'] == PRODUCTION_HOST_2:
        # No need to pull media twice
        return
    non_env_remote_media_path = _fetch_remote_variable(REMOTE_MEDIA_DIR)
    local_media_dir = os.getenv(ENV_MEDIA_DIR_VARIABLE)

    local('rsync -avz {}:{}/ {}'.format(env['host_string'],
                                        non_env_remote_media_path,
                                        local_media_dir))

deploy_staging = roles('staging')(_deploy)
deploy_live = roles('live')(_deploy)

pull_staging_data = roles('staging')(_pull_data)
pull_live_data = roles('live')(_pull_data)

pull_live_data_from_staging = roles('live')(_pull_live_data_from_staging)

pull_staging_media = roles('staging')(_pull_media)
pull_live_media = roles('live')(_pull_media)

pull_live_media_from_staging = roles('live')(_pull_live_media_from_staging)


@roles('live')
def purge_cache():
    run('ats-cache-purge torchbox.com')


@roles('staging')
def sync_staging_with_live():
    puts("This will backup then destroy all data on staging, and replace it with a duplicate of the production database.")
    if not confirm("Are you sure you want to continue?", default=False):
        puts("Phew! You got out of that one.")
        return
    env.forward_agent = True
    run('fab pull_live_data_from_staging')
    run("manage migrate --noinput")
    run('fab pull_live_media_from_staging')
    run('restart')
