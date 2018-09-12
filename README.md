Torchbox.com on Wagtail
=======================

[![Build Status](https://travis-ci.org/torchbox/wagtail-torchbox.svg?branch=master)](https://travis-ci.org/torchbox/wagtail-torchbox)

This project was originally a clone of [wagtaildemo](http://github.com/torchbox/wagtaildemo), customised for the Torchbox site.

Setup (with Vagrant)
--------------------

We recommend running Wagtail in a virtual machine using Vagrant, to ensure that the correct dependencies are in place.

### Dependencies
 - [VirtualBox](https://www.virtualbox.org/)
 - [Vagrant 1.1+](http://www.vagrantup.com)

### Installation

Run the following commands:

```bash
git clone [the url you copied above]
cd wagtail-torchbox
vagrant up
vagrant ssh

# then, within the SSH session:

./manage.py createcachetable
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```

To build static files you will additionally need to run the following commands:

```bash
cd /vagrant/tbx/core/static_src/
npm install
npm run build:prod
```

**Note:** You can run it within the VM where node is pre-installed, but if you are using Mac OS, you will likely have issues with performance of these commands. It is adviced to Mac OS users to have node on the host machine.

To install node on the host machine we recommend using [`nvm`](https://github.com/creationix/nvm). Once you have `nvm` installed simply run `nvm install` to install and activate the version of node required for the project. Refer to the nvm docs for more details about available commands.


After the installation the app will accessible on the host machine as http://localhost:8000/ - you can access the Wagtail admin interface at http://localhost:8000/admin/. The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

To make code changes:
 - Create a new branch for your work in the form `ticketnumber-briefdescription` e.g. `123-fix-dodgy-quotemarks`
 - Make your code changes
 - `git push origin branchname`
 - Go back to Torchbox repo in the browser (https://github.com/torchbox/wagtail-torchbox)
 - Click the big green 'New pull request' button
 - Set the 'base' as 'master' and the 'compare' as your branch.
 - Click 'create pull request.'

You will probably need to first merge to the staging branch in order to stage your changes and show them to the client. You still follow the process above, but add a comment to the pull request asking to manually merge to staging and deploy to the staging site. When you are ready to deploy, add another comment requesting that the pull request is merged to master and deployed.

### Download production data and media to local VM

Within the vagrant box:

```
heroku login
fab pull-production-data
fab pull-production-media
```

You may need to check on Heroku dashboard (https://dashboard.heroku.com) if you have the permission to access the `torchbox-production` app.
