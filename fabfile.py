from invoke.exceptions import Exit
from invoke.tasks import task


PRODUCTION_APP_INSTANCE = 'torchbox-production'


STAGING_APP_INSTANCE = 'torchbox-staging'
STAGING_APP_DB_INSTANCE = 'torchbox-staging'
STAGING_REMOTE = 'dokku@staging.torchbox.com'


LOCAL_MEDIA_FOLDER = '/vagrant/media'
LOCAL_DATABASE_NAME = 'torchbox'


############
# Production
############


@task
def pull_production_media(c):
    pull_media_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def push_production_media(c):
    raise RuntimeError('Please check the configuration of the fabfile before using it.')
    push_media_to_s3_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_data(c):
    pull_database_from_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def push_production_data(c):
    raise RuntimeError('Please check the configuration of the fabfile before using it.')
    push_database_to_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def deploy_production(c):
    raise RuntimeError('Please check the configuration of the fabfile before using it.')
    deploy_to_heroku(c, PRODUCTION_APP_INSTANCE, local_branch='master',
                     remote_branch='master')


@task
def production_shell(c):
    open_heroku_shell(c, PRODUCTION_APP_INSTANCE)


#########
# Staging
#########


@task
def pull_staging_data(c):
    pull_database_from_dokku(c, STAGING_REMOTE, STAGING_APP_DB_INSTANCE)


@task
def pull_staging_media(c):
    pull_media_from_s3_dokku(c, STAGING_REMOTE, STAGING_APP_INSTANCE)


@task
def push_staging_media(c):
    raise RuntimeError('Please check the configuration of the fabfile before using it.')
    push_media_to_s3_dokku(c, STAGING_REMOTE, STAGING_APP_INSTANCE)


@task
def push_staging_data(c):
    raise RuntimeError('Please check the configuration of the fabfile before using it.')
    push_database_to_dokku(c, STAGING_REMOTE, STAGING_APP_INSTANCE,
                           STAGING_APP_DB_INSTANCE)


@task
def deploy_staging(c):
    deploy_to_dokku(c, STAGING_REMOTE, STAGING_APP_INSTANCE,
                    local_branch='staging', remote_branch='staging')


@task
def staging_shell(c):
    open_dokku_shell(c, STAGING_REMOTE, STAGING_APP_INSTANCE)


#######
# Local
#######


def clean_local_database(c, local_database_name=LOCAL_DATABASE_NAME):
    c.run(
        'sudo -u postgres psql  -d {database_name} -c "DROP SCHEMA public '
        'CASCADE; CREATE SCHEMA public;"'.format(
            database_name=local_database_name
        )
    )


def delete_local_database(c, local_database_name=LOCAL_DATABASE_NAME):
    c.run('dropdb {database_name}'.format(
        database_name=LOCAL_DATABASE_NAME
    ), warn=True)


########
# Heroku
########


def get_heroku_variable(c, app_instance, variable):
    return c.run('heroku config:get {var} --app {app}'.format(
        app=app_instance,
        var=variable,
    )).stdout.strip()


def pull_media_from_s3_heroku(c, app_instance):
    aws_access_key_id = get_heroku_variable(c, app_instance,
                                            'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_heroku_variable(c, app_instance,
                                                'AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = get_heroku_variable(c, app_instance,
                                                  'AWS_STORAGE_BUCKET_NAME')
    pull_media_from_s3(c, aws_access_key_id, aws_secret_access_key,
                       aws_storage_bucket_name)


def push_media_to_s3_heroku(c, app_instance):
    prompt_msg = 'You are about to push your media folder contents to the ' \
                 'S3 bucket. It\'s a destructive operation. \n' \
                 'Please type the application name "{app_instance}" to ' \
                 'proceed:\n>>> '.format(app_instance=make_bold(app_instance))
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")
    aws_access_key_id = get_heroku_variable(c, app_instance,
                                            'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_heroku_variable(c, app_instance,
                                                'AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = get_heroku_variable(c, app_instance,
                                                  'AWS_STORAGE_BUCKET_NAME')
    push_media_to_s3(c, aws_access_key_id, aws_secret_access_key,
                     aws_storage_bucket_name)


def pull_database_from_heroku(c, app_instance):
    delete_local_database(c)
    c.run('heroku pg:pull --app {app} DATABASE_URL {local_database}'.format(
        app=app_instance,
        local_database=LOCAL_DATABASE_NAME
    ))


def push_database_to_heroku(c, app_instance):
    prompt_msg = 'You are about to push your local database to Heroku. ' \
                 'It\'s a destructive operation and will override the ' \
                 'database on the server. \n' \
                 'Please type the application name "{app_instance}" to ' \
                 'proceed:\n>>> '.format(app_instance=make_bold(app_instance))
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")
    c.run('heroku maintenance:on --app {app}'.format(app=app_instance))
    c.run('heroku ps:stop --app {app} web'.format(app=app_instance))
    c.run('heroku pg:backups:capture --app {app}'.format(app=app_instance))
    c.run('heroku pg:reset --app {app}'.format(app=app_instance))
    c.run('heroku pg:push --app {app}'.format(app=app_instance))
    c.run('heroku ps:restart --app {app}'.format(app=app_instance))
    c.run('heroku maintenance:off --app {app}'.format(app=app_instance))


def setup_heroku_git_remote(c, app_instance):
    remote_name = 'heroku-{app}'.format(app=app_instance)
    c.run('heroku git:remote --app {app} --remote {remote}'.format(
        app=app_instance, remote=remote_name
    ))
    return remote_name


def deploy_to_heroku(c, app_instance, local_branch='master',
                     remote_branch='master'):
    print(
        'This will push your local "{local_branch}" branch to remote '
        '"{remote_branch}" branch.'.format(
            local_branch=local_branch,
            remote_branch=remote_branch
        )
    )
    deploy_prompt(c, app_instance)
    remote_name = setup_heroku_git_remote(c, app_instance)
    c.run('git push {remote} {local_branch}:{remote_branch}'.format(
        remote=remote_name,
        local_branch=local_branch,
        remote_branch=remote_branch,
    ))


def open_heroku_shell(c, app_instance, shell_command='bash'):
    c.run('heroku run --app {app} {command}'.format(
        app=app_instance,
        command=shell_command,
    ))


#######
# Dokku
#######


def pull_database_from_dokku(c, dokku_remote, app_db_instance):
    clean_local_database(c)
    c.run('ssh {remote} postgres:export {db_instance} | '
          'pg_restore -d {local_database}'.format(
              remote=dokku_remote,
              db_instance=app_db_instance,
              local_database=LOCAL_DATABASE_NAME,
          ))


def push_database_to_dokku(c, dokku_remote, app_instance, db_instance):
    prompt_msg = 'You are about to push your local database to Dokku. ' \
                 'It\'s a destructive operation and will override the ' \
                 'database on the server. \n' \
                 'Please type the database name "{db_instance}" to ' \
                 'proceed:\n>>> '.format(db_instance=make_bold(db_instance))
    if input(prompt_msg) != db_instance:
        raise Exit("Aborted")
    c.run('ssh {remote} ps:stop {app}'.format(remote=dokku_remote,
                                              app=app_instance))
    clean_dokku_database(dokku_remote, db_instance)
    c.run(
        'pg_dump -Fc --no-acl --no-owner -w {local_db} | '
        'ssh -t {remote} postgres:import {db_instance} '
        '|| true'.format(
            local_db=LOCAL_DATABASE_NAME,
            remote=dokku_remote,
            db_instance=db_instance,
        )
    )
    c.run('ssh {remote} ps:start {app}'.format(remote=dokku_remote,
                                               app=app_instance))


def pull_media_from_s3_dokku(c, dokku_remote, app_instance):
    aws_access_key_id = get_dokku_variable(c, dokku_remote, app_instance,
                                           'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_dokku_variable(c, dokku_remote, app_instance,
                                               'AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = get_dokku_variable(c, dokku_remote, app_instance,
                                                 'AWS_STORAGE_BUCKET_NAME')
    pull_media_from_s3(c, aws_access_key_id, aws_secret_access_key,
                       aws_storage_bucket_name)


def push_media_to_s3_dokku(dokku_remote, app_instance):
    prompt_msg = 'You are about to push your media folder contents to the ' \
                 'S3 bucket. It\'s a destructive operation. \n' \
                 'Please type the application name "{app_instance}" to ' \
                 'proceed:\n>>> '.format(app_instance=make_bold(app_instance))
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")
    aws_access_key_id = get_dokku_variable(dokku_remote, app_instance,
                                           'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_dokku_variable(dokku_remote, app_instance,
                                               'AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = get_dokku_variable(dokku_remote, app_instance,
                                                 'AWS_STORAGE_BUCKET_NAME')
    push_media_to_s3(aws_access_key_id, aws_secret_access_key,
                     aws_storage_bucket_name)


def get_dokku_variable(c, dokku_remote, app_instance, variable):
    return c.run('ssh {remote} config:get {app} {var}'.format(
        remote=dokku_remote,
        app=app_instance,
        var=variable,
    )).stdout.strip()


def deploy_to_dokku(c, dokku_remote, app_instance, local_branch='master',
                    remote_branch=None):
    if remote_branch is None:
        remote_branch = local_branch
    print(
        'This will push your local "{local_branch}" branch to remote '
        '"{remote_branch}" branch.'.format(
            local_branch=local_branch,
            remote_branch=remote_branch
        )
    )
    deploy_prompt(c, app_instance)
    c.run('git push {remote}:{app} {local_branch}:{remote_branch}'.format(
        remote=dokku_remote,
        app=app_instance,
        local_branch=local_branch,
        remote_branch=remote_branch,
    ))


def open_dokku_shell(c, dokku_remote, app_instance):
    c.run('ssh -t {remote} enter {app}'.format(remote=dokku_remote,
                                               app=app_instance))


def clean_dokku_database(c, dokku_remote, db_instance):
    c.run(
        'ssh -t {remote} postgres:export {db_instance} > '
        '{db_instance}-backup.pg'.format(
            remote=dokku_remote,
            db_instance=db_instance,
        )
    )
    c.run(
        'echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | '
        'ssh -t {remote} postgres:connect {db_instance}'.format(
            remote=dokku_remote,
            db_instance=db_instance,
        )
    )


####
# S3
####


def aws(c, command, aws_access_key_id, aws_secret_access_key, **kwargs):
    return c.run(
        'AWS_ACCESS_KEY_ID={access_key_id} AWS_SECRET_ACCESS_KEY={secret_key} '
        'aws {command}'.format(
            access_key_id=aws_access_key_id,
            secret_key=aws_secret_access_key,
            command=command,
        ),
        **kwargs
    )


def pull_media_from_s3(c, aws_access_key_id, aws_secret_access_key,
                       aws_storage_bucket_name,
                       local_media_folder=LOCAL_MEDIA_FOLDER):
    aws_cmd = 's3 sync --delete s3://{bucket_name} {local_media}'.format(
        bucket_name=aws_storage_bucket_name,
        local_media=local_media_folder,
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


def push_media_to_s3(c, aws_access_key_id, aws_secret_access_key,
                     aws_storage_bucket_name,
                     local_media_folder=LOCAL_MEDIA_FOLDER):
    aws_cmd = 's3 sync --delete {local_media} s3://{bucket_name}/'.format(
        bucket_name=aws_storage_bucket_name,
        local_media=local_media_folder,
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


###########
# Utilities
###########

def deploy_prompt(c, app_instance):
    prompt_msg = 'You are about to do a manual deployment. You probably ' \
                 'should use automatic deployments on CI. \nPlease type ' \
                 'the application name "{app_instance}" in order to ' \
                 'proceed:\n>>> '.format(app_instance=make_bold(app_instance))
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")


def make_bold(msg):
    return "\033[1m{}\033[0m".format(msg)
