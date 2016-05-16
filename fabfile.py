from __future__ import with_statement

import uuid

from fabric.api import env, get, local, puts, roles, run

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
REMOTE_PROJECT_PATH = '$D/'
REMOTE_DUMP_PATH = '{}tmp/'.format(REMOTE_PROJECT_PATH)
REMOTE_MEDIA_DIR = '$CFG_MEDIA_DIR'


def _fetch_remote_variable(input_string):
    """ Runs `echo $SOMEVAR`, with no terminal assigned, so that the server
    doesn't add extra bumf to stdout.
    """
    return run('echo {}'.format(input_string), pty=False)


def _fetch_local_variable(input_string):
    """ Runs `echo $SOMEVAR`, with no terminal assigned, so that the server
    doesn't add extra bumf to stdout.
    """
    return local('echo {}'.format(input_string))


def _deploy():

    if env['host'] == STAGING_HOST:
        branch = 'staging'
    else:
        branch = 'master'

    run('git pull origin {}'.format(branch))
    run('pip install -r requirements.txt')
    run('dj migrate --noinput')
    run('dj collectstatic --noinput')
    run('dj compress')
    run('dj update_index')
    run('restart')


def _pull_data():
    if env['host'] == PRODUCTION_HOST_2:
        # No need to pull data twice
        return

    local_db_name = _fetch_local_variable(REMOTE_DB_NAME) or LOCAL_DB_NAME
    local_dump_path = _fetch_local_variable(REMOTE_DUMP_PATH) or LOCAL_DUMP_PATH

    filename = "{}-{}.sql".format(PROJECT_NAME, uuid.uuid4())
    local_path = "{}{}".format(local_dump_path, filename)
    remote_path = "{}{}".format(REMOTE_DUMP_PATH, filename)
    local_db_backup_path = "{}vagrant-{}-{}.sql".format(local_dump_path, local_db_name, uuid.uuid4())
    non_env_remote_path = _fetch_remote_variable(remote_path)

    run('pg_dump -U{} -xOf {} {}'.format(REMOTE_DB_USERNAME, remote_path, REMOTE_DB_NAME))
    run('gzip {}'.format(remote_path))
    get("{}.gz".format(non_env_remote_path), "{}.gz".format(local_path))
    run('rm {}.gz'.format(remote_path))

    local('pg_dump -xOf {} {}'.format(local_db_backup_path, local_db_name))
    puts('Previous local database backed up to {}'.format(local_db_backup_path))

    local('dropdb {}'.format(local_db_name))
    local('createdb {}'.format(local_db_name))
    local('gunzip {}.gz'.format(local_path))
    local('psql {} -f {}'.format(local_db_name, local_path))
    local('rm {}'.format(local_path))


def _pull_media():
    if env['host'] == PRODUCTION_HOST_2:
        # No need to pull media twice
        return
    non_env_remote_media_path = _fetch_remote_variable(REMOTE_MEDIA_DIR)
    local('rm -rf media.old')
    local_media_dir = _fetch_local_variable(REMOTE_MEDIA_DIR) or LOCAL_MEDIA_DIR
    local('cp -r {} {}.old || true'.format(local_media_dir, local_media_dir))

    local('rsync -avz %s:%s /vagrant/media/' % (env['host_string'], non_env_remote_media_path))


deploy_staging = roles('staging')(_deploy)
deploy_live = roles('live')(_deploy)

pull_staging_data = roles('staging')(_pull_data)
pull_live_data = roles('live')(_pull_data)

pull_staging_media = roles('staging')(_pull_media)
pull_live_media = roles('live')(_pull_media)


@roles('live')
def purge_cache():
    run('ats-cache-purge torchbox.com')


@roles('staging')
def sync_staging_with_live():
    env.forward_agent = True
    run('fab pull_live_data')
    run("manage migrate --noinput")
    run('fab pull_live_media')
