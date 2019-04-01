Torchbox.com on Wagtail
=======================

[![Build Status](https://travis-ci.org/torchbox/wagtail-torchbox.svg?branch=master)](https://travis-ci.org/torchbox/wagtail-torchbox)

This project is the backend element for the new Torchbox.com site, the [Front-end](https://github.com/torchbox/torchbox-frontend/) is built with Gatsby and consumes the CMS's content via GraphQL. 

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

After the installation the app will accessible on the host machine as http://localhost:8000/admin. The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.


### Download production data and media to local VM

Within the vagrant box:

```
heroku login
fab pull-production-data
fab pull-production-media
```

You may need to check on Heroku dashboard (https://dashboard.heroku.com) if you have the permission to access the `cms-torchbox-com` app.


Site Architecture
-----------------

In this project Wagtail is used as a headless CMS and it's data is consumed via [GraphQL](https://graphql.org/). This means that to preview any UI changes on the site you'll also need to setup the [frontend](https://github.com/torchbox/torchbox-frontend/) component.

### What's different here?

Any Django/Wagtail specific development is the same (Models, Snippets, Taxonomies etc) except how this data is accessed. Instead of using data in a django template, we explicity define what data is available to query via GraphQL in the `./tbx/graphql/schema.py` file. If you have done any work with [Graphene](https://docs.graphene-python.org/en/latest/) before then this file will look fairly standard, if not, please take a look through this [simple demo](https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/) to improve your understanding of how to build on the GraphQL api.


### ...and the frontend?

As mentioned above, the [frontend](https://github.com/torchbox/torchbox-frontend/) is a seperate project built with [Gatsby](https://www.gatsbyjs.org/). If you want to really know how Gatsby works then you can find out [here](https://www.gatsbyjs.org/docs/behind-the-scenes/) but the basics that you need to know is that Gatsby is a modern static site builder for React that enables you to build blazingly fast sites while keeping the 'reactness' of a React app.

The HTML of each page is generated in node during the build process. This means when the user opens the page in a browser that the page renders instantly (because it isn't reliant on JS to bootstrap the page, the HTML is ready to go!) but when JS executes on the page everything becomes dynamic like a traditional React app.


### Where does it live?

This project (the backend) is deployed on heroku and is automatically deployed when the `new` branch is updated. The frontend is hosted on [Netlify](https://www.netlify.com/) and is also linked to the frontend repo for auto deployment (new netlify builds are also triggered by a page publish in Wagtail). Netlify will also create 'deploy previews' whenever an MR is created so that you can preview your changes before you merge!


### What order should I develop in?

When developing a new feature such as a Page model (with accompanying UI), the best approach will to build the models, graphql schema (again follow the tutorial above if you're confused by this) with the project running locally. Once you've finished your backend then start developing the frontend by pointing the Gatsby project at your local GraphQL endpoint. Once both sides of the feature are done, get your backend reviewed and pushed to Production/Staging. Once your backend is public you can then submit your frontend for review because Netlfiy will be able to build a preview of the branch with the right data (The gatsby build will fail if the GraphQL queries don't match up with the backend!).
