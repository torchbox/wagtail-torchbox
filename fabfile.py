from __future__ import with_statement
from fabric.api import *

import uuid

env.roledefs = {
    'staging': ['django-staging.torchbox.com'],
    'production': ['tbxwagtail@by-web-2.torchbox.com'],
}

LIVE_DB_USERNAME = "tbxwagtail"
LIVE_DB_SERVER = "by-postgres-a"
DB_NAME = "wagtail-torchbox"
LOCAL_DUMP_PATH = "~/"
REMOTE_DUMP_PATH = "~/"

@roles('staging')
def deploy_staging():
    with cd('/usr/local/django/tbxwagtail/'):
        with settings(sudo_user='tbxwagtail'):
            sudo("git pull")
            sudo("git submodule update")
            sudo("/usr/local/django/virtualenvs/tbxwagtail/bin/pip install -r requirements/production.txt")
            sudo("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py syncdb --settings=tbx.settings.production --noinput")
            sudo("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py migrate --settings=tbx.settings.production --noinput")
            sudo("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py collectstatic --settings=tbx.settings.production --noinput")
            sudo("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py compress --force --settings=tbx.settings.production")

        sudo("supervisorctl restart tbxwagtail")

@roles('production')
def deploy():
    with cd('/usr/local/django/tbxwagtail/'):
        run("git pull")
        run("git submodule update")

        run("/usr/local/django/virtualenvs/tbxwagtail/bin/pip install -r requirements/production.txt")
        run("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py syncdb --settings=tbx.settings.production --noinput")
        run("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py migrate --settings=tbx.settings.production --noinput")
        run("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py collectstatic --settings=tbx.settings.production --noinput")
        run("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py compress --settings=tbx.settings.production")

    run("sudo supervisorctl restart tbxwagtail")
    #sudo("/usr/local/django/virtualenvs/tbxwagtail/bin/python manage.py update_index --settings=tbx.settings.production")

@roles('production')
def pull_live_data():
    filename = "%s-%s.sql" % (DB_NAME, uuid.uuid4())
    local_path = "%s%s" % (LOCAL_DUMP_PATH, filename)
    remote_path = "%s%s" % (REMOTE_DUMP_PATH, filename)
    local_db_backup_path = "%svagrant-%s-%s.sql" % (LOCAL_DUMP_PATH, DB_NAME, uuid.uuid4())

    run('pg_dump -U%s -h %s -xOf %s' % (LIVE_DB_USERNAME, LIVE_DB_SERVER, remote_path))
    run('gzip %s' % remote_path)
    get("%s.gz" % remote_path, "%s.gz" % local_path)
    run('rm %s.gz' % remote_path)
    
    local('pg_dump -Upostgres -cf %s %s' % (local_db_backup_path, DB_NAME))
    puts('Previous local database backed up to %s' % local_db_backup_path)
    
    local('dropdb -Upostgres %s' % DB_NAME)
    local('createdb -Upostgres %s' % DB_NAME)
    local('gunzip %s.gz' % local_path)
    local('psql -Upostgres %s -f %s' % (DB_NAME, local_path))
    local ('rm %s' % local_path)

@roles('production')
def push_live_data():
    filename = "%s-%s.sql" % (DB_NAME, uuid.uuid4())
    local_path = "%s%s" % (LOCAL_DUMP_PATH, filename)
    remote_path = "%s%s" % (REMOTE_DUMP_PATH, filename)
    live_db_backup_path = "%s%s-%s.sql" % (REMOTE_DUMP_PATH, DB_NAME, uuid.uuid4())

    local('pg_dump -Upostgres -xOf %s %s' % (local_path, DB_NAME))
    local('gzip %s' % local_path)
    put("%s.gz" % local_path, "%s.gz" % remote_path)

    run('pg_dump -xO -U%s -h %s -f %s' % (LIVE_DB_USERNAME, LIVE_DB_SERVER, live_db_backup_path))
    puts('Previous live database backed up to %s' % live_db_backup_path)
    
    run('gunzip %s.gz' % remote_path)
    run('psql -U%s -h %s -c "DROP SCHEMA public CASCADE"' % (LIVE_DB_USERNAME, LIVE_DB_SERVER))
    run('psql -U%s -h %s -c "CREATE SCHEMA public"' % (LIVE_DB_USERNAME, LIVE_DB_SERVER))
    run('psql -U%s -h %s -f %s' % (LIVE_DB_USERNAME, LIVE_DB_SERVER, remote_path))
    run('rm %s' % remote_path)
