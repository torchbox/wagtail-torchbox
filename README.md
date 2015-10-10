Torchbox.com on Wagtail
=======================

[Wagtail](http://wagtail.io) is distributed as a Python package, to be incorporated into a Django project via the INSTALLED_APPS setting. To get you up and running quickly, we provide a demo site with all the configuration in place, including a set of example page types.

This project is essentially a clone of [wagtaildemo](http://github.com/torchbox/wagtaildemo), customised for the torchbox site.

Setup (with Vagrant)
-----

We recommend running Wagtail in a virtual machine using Vagrant, as this ensures that the correct dependencies are in place regardless of how your host machine is set up.

### Dependencies
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant 1.1+](http://www.vagrantup.com)

### Installation
Run the following commands:

    git clone https://github.com/torchbox/wagtail-torchbox.git
    cd wagtail-torchbox
    vagrant up
    vagrant ssh
      (then, within the SSH session:)
    ./manage.py createsuperuser
    ./manage.py runserver 0.0.0.0:8000

This will make the app accessible on the host machine as http://localhost:8000/ - you can access the Wagtail admin interface at http://localhost:8000/admin/ . The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.
