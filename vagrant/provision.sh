#!/bin/sh
set -xe

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


# Create database
set +e
su - vagrant -c "createdb $PROJECT_NAME"
set -e

# Replace previous line with this if you are using Python 2
su - vagrant -c "virtualenv --python=python3 $VIRTUALENV_DIR"

su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"


# Install PIP requirements
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements.txt"

# Install Fabric 2
apt-get remove -y fabric
su - vagrant -c "$PIP install Fabric==2.1.3"

# Install Heroku CLI
curl -sSL https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install AWS CLI
apt-get update -y
apt-get install -y unzip
rm -rf /tmp/awscli-bundle || true
rm -rf /tmp/awscli-bundle.zip || true
curl -sSL "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "/tmp/awscli-bundle.zip"
unzip /tmp/awscli-bundle.zip -d /tmp
/tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=tbx.settings.dev

alias dj="django-admin.py"
alias djrun="dj runserver 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF


# Install node.js and npm
curl -sSL https://deb.nodesource.com/setup_4.x | bash -
apt-get install -y nodejs

# Build the static files
if [ -d "$PROJECT_DIR/node_modules" ]; then
    rm -rf "$PROJECT_DIR/node_modules"
fi
su - vagrant -c "cd $PROJECT_DIR; npm install"
su - vagrant -c "cd $PROJECT_DIR; npm run build:prod"
