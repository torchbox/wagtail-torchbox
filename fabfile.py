from __future__ import with_statement
from fabric.api import *

import uuid

env.roledefs = {
    'staging': ['django-staging.torchbox.com'],
}

@roles('staging')
def deploy_staging():
    with cd('/usr/local/django/wagtail-torchbox/'):
        with settings(sudo_user='wagtail-torchbox'):
            sudo("git pull")
            sudo("git submodule update")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/pip install -r requirements/production.txt")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py syncdb --settings=tbx.settings.staging --noinput")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py migrate --settings=tbx.settings.staging --noinput")
            sudo("/usr/local/django/virtualenvs/wagtail-torchboxwagtail-torchbox/bin/python manage.py collectstatic --settings=tbx.settings.staging --noinput")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py compress --settings=tbx.settings.staging")

        sudo("supervisorctl restart wagtail-torchbox")
        sudo("supervisorctl restart tbx-celeryd")
        sudo("supervisorctl restart tbx-celerybeat")

        with settings(sudo_user='wagtail-torchbox'):
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py update_index --settings=tbx.settings.staging")


@roles('production')
def deploy():
    with cd('/usr/local/django/wagtail-torchbox/'):
        with settings(sudo_user='wagtail-torchbox'):
            sudo("git pull")
            sudo("git submodule update")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/pip install -r requirements/production.txt")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py syncdb --settings=tbx.settings.production --noinput")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py migrate --settings=tbx.settings.production --noinput")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py collectstatic --settings=tbx.settings.production --noinput")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py compress --settings=tbx.settings.production")

            run("supervisorctl restart wagtail-torchbox")
            run("supervisorctl restart tbx-celeryd")
            run("supervisorctl restart tbx-celerybeat")
            sudo("/usr/local/django/virtualenvs/wagtail-torchbox/bin/python manage.py update_index --settings=tbx.settings.production")

@roles('db')
def fetch_live_data():
    pass
    # filename = "wagtail_torchbox_%s.sql" % uuid.uuid4()
    # local_path = "/home/vagrant/verdant/%s" % filename
    # remote_path = "/root/dumps/%s" % filename

    # run('pg_dump -Upostgres -cf %s verdant_rca' % remote_path)
    # run('gzip %s' % remote_path)
    # get("%s.gz" % remote_path, "%s.gz" % local_path)
    # run('rm %s.gz' % remote_path)
    # local('dropdb -Upostgres verdant')
    # local('createdb -Upostgres verdant')
    # local('gunzip %s.gz' % local_path)
    # local('psql -Upostgres verdant -f %s' % local_path)
    # local ('rm %s' % local_path)
