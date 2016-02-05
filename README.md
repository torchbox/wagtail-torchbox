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
 - Go back to Torchbox repo in the browser (https://github.com/torchbox/wagtail-torchbox)
 - Click the big green 'New pull request' button
 - Set the 'base' as 'master' and the 'compare' as your branch.
 - Click 'create pull request.'

You will probably need to first merge to the staging branch in order to stage your changes and show them to the client. You still follow the process above, but add a comment to the pull request asking to manually merge to staging and deploy to the staging site. When you are ready to deploy, add another comment requesting that the pull request is merged to master and deployed.
