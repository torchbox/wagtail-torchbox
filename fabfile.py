import os
import subprocess

from invoke import run as local
from invoke.exceptions import Exit
from invoke.tasks import task


# Process .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            var, value = line.strip().split("=", 1)
            os.environ.setdefault(var, value)


FRONTEND = os.getenv("FRONTEND", "docker")

PROJECT_DIR = "/app"

PRODUCTION_APP_INSTANCE = "cms-torchbox-com"
STAGING_APP_INSTANCE = "torchbox-staging"

LOCAL_MEDIA_FOLDER = os.path.join(PROJECT_DIR, "media")
LOCAL_IMAGES_FOLDER = os.path.join(LOCAL_MEDIA_FOLDER, "original_images")
LOCAL_DATABASE_NAME = "tbx"
LOCAL_DATABASE_USERNAME = "tbx"
LOCAL_DUMP_FOLDER = "database_dumps"
PROJECT_NAME = "tbx"

############
# Docker
############


def dexec(cmd, service="web", **kwargs):
    return local(
        'docker-compose exec -T {} bash -c "{}"'.format(service, cmd), **kwargs
    )


def sudexec(cmd, service="web", **kwargs):
    return local(
        'docker-compose exec --user root -T {} bash -c "{}"'.format(service, cmd),
        **kwargs
    )


@task
def build(c):
    """
    Build the development environment (call this first)
    """
    local("mkdir -p media")
    local("docker-compose up -d --build")
    provision(c)
    local("docker-compose stop")
    print("Project built: now run 'fab up'")


@task
def build_web(c):
    """
    Build the web container only.
    """
    local("mkdir -p media")
    local("docker-compose up -d --build web")
    provision(c)
    local("docker-compose stop")
    print("Project built: now run 'fab up'")


def provision(c):
    # Install Heroku CLI
    sudexec("curl -sSL https://cli-assets.heroku.com/install-ubuntu.sh | sh")

    # Install AWS CLI
    sudexec("apt-get install -y unzip")
    sudexec("rm -rf /tmp/awscli-bundle || true")
    sudexec("rm -rf /tmp/awscli-bundle.zip || true")
    sudexec(
        "curl -sSL 'https://s3.amazonaws.com/aws-cli/awscli-bundle.zip' -o '/tmp/awscli-bundle.zip'"
    )
    sudexec("unzip -q /tmp/awscli-bundle.zip -d /tmp")
    sudexec("/tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws")

    # Create home dir so Heroku CLI stays happy
    sudexec("mkdir -p /home/{}".format("tbx"))
    sudexec("chmod 775 /home/{}".format("tbx"))
    sudexec("chown -R {0}:{0} /home/{0}".format("tbx"))

    # Install Postgres client
    sudexec("apt install -y postgresql-client")

    # Setup a bash alias
    dexec("echo 'alias dj=\'python manage.py\'' >> ~/.bashrc")


@task
def up(c):
    """
    Start the development environment
    """
    # ensure the media mount directory exists in case it's been removed since build-time
    local("mkdir -p media")
    local("docker-compose up -d")


@task
def stop(c):
    """
    Stop the development environment
    """
    local("docker-compose stop")


@task
def destroy(c):
    """
    Destroy development environment containers (media and DB will be kept until you run `docker volume prune`)
    """
    local("docker-compose down")


@task
def ssh(c):
    """
    Run bash in the web container
    """
    subprocess.call("docker-compose exec web bash", shell=True)


@task
def ssh_root(c):
    """
    Run bash as root in the web container
    """
    subprocess.call("docker-compose exec --user root web bash", shell=True)


@task
def pdb(c):
    """
    Run web container allowing for pdb callbacks.
    """
    subprocess.call("docker-compose run --service-ports web", shell=True)


@task
def heroku_login(c):
    """
    Log into the Heroku app for accessing config vars, database backups etc.
    """
    subprocess.call("docker-compose exec web heroku login", shell=True)


@task
def psql(c):
    """
    Connect to the postgres DB using psql
    """
    subprocess.call(
        "docker-compose exec --user postgres db psql -U{local_database} -d{local_database}".format(
            local_database=LOCAL_DATABASE_NAME
        ),
        shell=True,
    )


@task
def psql_query(c, query):
    """
    Run a query against the postgres DB using psql
    """
    subprocess.call(
        'docker-compose exec --user postgres db psql -U{local_database} -d{local_database} -c "{query}"'.format(
            local_database=LOCAL_DATABASE_NAME, query=query
        ),
        shell=True,
    )


#######
# Local
#######


def delete_local_database(c, local_database_name=LOCAL_DATABASE_NAME):
    local("docker-compose stop web")
    dexec(
        "dropdb --if-exists --host db --username={project_name} {database_name}".format(
            project_name=PROJECT_NAME, database_name=LOCAL_DATABASE_NAME
        ),
        "db",
    )
    dexec(
        "createdb --host db --username={project_name} {database_name}".format(
            project_name=PROJECT_NAME, database_name=LOCAL_DATABASE_NAME
        ),
        "db",
    )
    local("docker-compose start web")


####
# S3
####


def aws(c, command, aws_access_key_id, aws_secret_access_key, **kwargs):
    return dexec(
        "AWS_ACCESS_KEY_ID={access_key_id} AWS_SECRET_ACCESS_KEY={secret_key} "
        "aws {command}".format(
            access_key_id=aws_access_key_id,
            secret_key=aws_secret_access_key,
            command=command,
        ),
        **kwargs
    )


def pull_media_from_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_media_folder=LOCAL_MEDIA_FOLDER,
):
    aws_cmd = "s3 sync --delete s3://{bucket_name} {local_media}".format(
        bucket_name=aws_storage_bucket_name, local_media=local_media_folder,
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)
    # The above command just syncs the original images: this clears the wagtailimages_renditions
    # table so that the renditions will be re-created when requested on the local build.
    delete_local_renditions(c)


def push_media_to_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_media_folder=LOCAL_MEDIA_FOLDER,
):
    aws_cmd = "s3 sync --delete {local_media} s3://{bucket_name}/".format(
        bucket_name=aws_storage_bucket_name, local_media=local_media_folder,
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


def pull_images_from_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_images_folder=LOCAL_IMAGES_FOLDER,
):
    aws_cmd = "s3 sync --delete s3://{bucket_name}/original_images {local_media}".format(
        bucket_name=aws_storage_bucket_name, local_media=local_images_folder
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)
    # The above command just syncs the original images: this clears the wagtailimages_renditions
    # table so that the renditions will be re-created when requested on the local build.
    delete_local_renditions(c)


########
# Heroku
########


def check_if_logged_in_to_heroku(c):
    if not dexec("heroku auth:whoami", warn=True):
        raise Exit(
            'Log-in with the "fab heroku-login" command before running this ' "command."
        )


def get_heroku_variable(c, app_instance, variable):
    check_if_logged_in_to_heroku(c)
    return local(
        "heroku config:get {var} --app {app}".format(app=app_instance, var=variable)
    ).stdout.strip()


def pull_media_from_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "AWS_STORAGE_BUCKET_NAME"
    )
    pull_media_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )


def pull_images_from_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "AWS_STORAGE_BUCKET_NAME"
    )
    pull_images_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )


def pull_database_from_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    delete_local_database(c)

    dexec(
        "heroku pg:backups:download --output=/tmp/dump --app {app}".format(
            app=app_instance
        )
    )
    dexec(
        "pg_restore --clean --no-acl --if-exists --no-owner --host db "
        "--username={project_name} -d {database_name} /tmp/dump".format(
            project_name=PROJECT_NAME, database_name=LOCAL_DATABASE_NAME
        )
    )
    dexec("rm /tmp/dump")
    print(
        "Any superuser accounts you previously created locally will have been wiped and will need to be recreated."
    )


def push_database_to_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    prompt_msg = (
        "You are about to push your local database to Heroku. "
        "It's a destructive operation and will override the "
        "database on the server. \n"
        'Please type the application name "{app_instance}" to '
        "proceed:\n>>> ".format(app_instance=app_instance)
    )
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")
    local("heroku maintenance:on --app {app}".format(app=app_instance))
    local("heroku ps:stop --app {app} web".format(app=app_instance))
    local("heroku pg:backups:capture --app {app}".format(app=app_instance))
    local("heroku pg:reset --app {app} --confirm {app}".format(app=app_instance))
    local(
        "heroku pg:push --app {app} {local_db} DATABASE_URL".format(
            app=app_instance, local_db=LOCAL_DATABASE_NAME
        )
    )
    local("heroku ps:restart --app {app}".format(app=app_instance))
    local("heroku maintenance:off --app {app}".format(app=app_instance))


def delete_local_renditions(c):
    try:
        psql_query(c, "DELETE FROM images_rendition;")
    except Exception:
        pass

    try:
        psql_query(c, "DELETE FROM wagtailimages_rendition;")
    except Exception:
        pass


def open_heroku_shell(c, app_instance, shell_command="bash"):
    raise Exit('Run "heroku run bash -a {}"'.format(app_instance))


#########
# Staging
#########


@task
def pull_staging_media(c):
    """Pull media from staging AWS S3"""
    pull_media_from_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def pull_staging_images(c):
    """Pull images from staging AWS S3"""
    pull_images_from_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def pull_staging_data(c):
    """Pull database from staging Heroku Postgres"""
    pull_database_from_heroku(c, STAGING_APP_INSTANCE)


@task
def staging_shell(c):
    """Connect to a shell prompt on Heroku staging"""
    open_heroku_shell(c, STAGING_APP_INSTANCE)


#########
# Production
#########


@task
def pull_production_media(c):
    """Pull media from staging AWS S3"""
    pull_media_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_images(c):
    """Pull images from production AWS S3"""
    pull_images_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_data(c):
    """Pull database from production Heroku Postgres"""
    pull_database_from_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def production_shell(c):
    """Connect to a shell prompt on Heroku production"""
    open_heroku_shell(c, PRODUCTION_APP_INSTANCE)
