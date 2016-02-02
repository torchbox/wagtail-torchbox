Torchbox.com on Wagtail
=======================

[![Build Status](http://ci.torchbox.com/api/badges/torchbox/wagtail-torchbox/status.svg)](http://ci.torchbox.com/torchbox/wagtail-torchbox)

[Wagtail](http://wagtail.io) is distributed as a Python package, to be incorporated into a Django project via the INSTALLED_APPS setting. To get you up and running quickly, we provide a demo site with all the configuration in place, including a set of example page types.

This project is essentially a clone of [wagtaildemo](http://github.com/torchbox/wagtaildemo), customised for the torchbox site.

Setup (with Vagrant)
-----

We recommend running Wagtail in a virtual machine using Vagrant, as this ensures that the correct dependencies are in place regardless of how your host machine is set up.

### Dependencies
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant 1.1+](http://www.vagrantup.com)

### Installation

Only Tech Team members can push to the repository. To make a change please fork the repository then make a pull request.

**Note you'll need to make a new fork and build for each new piece of work you do.**

    - Visit https://github.com/torchbox/wagtail-torchbox in your browser
    - Click 'fork' (top right)
    - It will ask you where to clone the repo to - choose your username
    - Find the url of your cloned repo (next to the ssh dropdown). It will be something like

    git@github.com:helenb/wagtail-torchbox.git

Run the following commands:
	
    git clone [the url you copied above]
    cd wagtail-torchbox
    vagrant up
    vagrant ssh
      (then, within the SSH session:)
    ./manage.py createsuperuser
    ./manage.py runserver 0.0.0.0:8000

This will make the app accessible on the host machine as http://localhost:8000/ - you can access the Wagtail admin interface at http://localhost:8000/admin/ . The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

To make coding changes:

    - Create a new branch for your work in the form `ticketnumber-briefdescription` e.g. `123-fix-dodgy-quotemarks`
    - Make your code changes, add and commit them to your branch.
    - `git push origin branchname`
    - Go back to the original Torchbox repo in the browser (https://github.com/torchbox/wagtail-torchbox)
    - Click the big green 'New pull request' button
    - Click the link that says 'compare across forks'.
    - For the base fork choose the fork on the tbx codebase you want to merge into, e.g. staging. For the head fork choose your new branch.
    - It will show you the changes. Click 'Create pull request'.

