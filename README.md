Torchbox.com on Wagtail
=======================

[![Build Status](http://ci.torchbox.com/api/badges/torchbox/wagtail-torchbox/status.svg)](http://ci.torchbox.com/torchbox/wagtail-torchbox)

This project was originally a clone of [wagtaildemo](http://github.com/torchbox/wagtaildemo), customised for the Torchbox site.

Setup (with Vagrant)
--------------------

We recommend running Wagtail in a virtual machine using Vagrant, to ensure that the correct dependencies are in place.

### Dependencies
 - [VirtualBox](https://www.virtualbox.org/)
 - [Vagrant 1.1+](http://www.vagrantup.com)

### Installation

Only Tech Team members can push to the repository. To make a change please fork the repository then make a pull request.
 - Visit https://github.com/torchbox/wagtail-torchbox in your browser
 - Click 'Fork' (top right)
 - It will ask you where to clone the repo to - choose your username
 - Find the URL of your cloned repo (next to the SSH dropdown). It will be something like

    `git@github.com:helenb/wagtail-torchbox.git`

Run the following commands:
	
```
git clone [the url you copied above]
cd wagtail-torchbox
vagrant up
vagrant ssh
# then, within the SSH session:
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```

This will make the app accessible on the host machine as http://localhost:8000/ - you can access the Wagtail admin interface at http://localhost:8000/admin/. The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

To make code changes:
 - Create a new branch for your work in the form `ticketnumber-briefdescription` e.g. `123-fix-dodgy-quotemarks`
 - Make your code changes
 - `git push origin branchname`
 - Go back to the original Torchbox repo in the browser (https://github.com/torchbox/wagtail-torchbox)
 - Click the big green 'New pull request' button
 - Click the link that says 'compare across forks'.
