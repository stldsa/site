# St. Louis DSA Website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the codesbas for the St Louis DSA website! We hope this guide will make it easy for newcomers to contribute to website features.

## Before You Begin

Right now, our website is primarily built using Python, particularly the Django web development framework. If you would like to develop tools using a different language or framework, please reach out to tech@stldsa.org and set up a meeting with a Tech Committee Chair so we can help you get started.

### Learning about Django

 If you'd like to learn the basics of Django, their [official tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) is excellent.

### Wagtail CMS

Many pages on our site are built with Wagtail, which is a nice Django-based content management system (CMS) designed to make it easier for non-programmers to update content on the site - read about the [Zen of Wagtail](https://docs.wagtail.io/en/stable/getting_started/the_zen_of_wagtail.html) to get the idea.

## Getting Set Up

The easiest way to get started with your local development environment is through our Docker Setup, which is outlined below. If these instructions do not work (or if you'd like to set up your own environment and have questions), please reach out to tech@stldsa.org or make a pull request with suggested changes.

### 1. Clone the repository

i.e.,

    git clone https://github.com/stldsa/site.git

If you are a member of DSA, ask to be added as a maintainer of the repo. If you are not a member, feel free to fork the repo.

### 2. [Install Docker](https://docs.docker.com/engine/install/)

### 3. Build your Docker Image and spin up a container

Depending your development preferences, you can choose one of the following options:

1. Use [VS Code](https://code.visualstudio.com/) as your IDE and install the [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Opening the project folder in VS Code will now invite you to open the folder in a Dev Container. Easy peasy.

2. If you'd like to use your own IDE and command line utility, you can run your containers using [docker-compose](https://docs.docker.com/compose/install/):

      `docker-compose up`

   In a new terminal window, you can run a command in the docker container using: 
   
      `docker-compose run web <command>`
      
   Or you might wish to create an alias:

      - Linux (bash) : `echo 'function stldsa() { docker-compose run web "$@"; }' >> ~/.bashrc`
      - macOS (Terminal) : `echo 'function stldsa() { docker-compose run web "$@"; }' >> ~/.bash_profile`

   Restart your terminal window for the alias to take effect. You may now simply run commands with  `stldsa <command>`. 

   When you're done with your session, you can run `docker-compose stop` to stop the running container or `docker-compose down` to remove the container completely (this will delete any data or settings you may have added).

### 4. Initialize Database

To get our application working, we need to initialize our database schema with a [migration](https://docs.djangoproject.com/en/3.2/topics/migrations/):

    python manage.py migrate

Now we need to seed our database with some fake data:

    stldsa python manage.py seed-db
      
 You should now be able to view a functional copy of the website in your browser at http://localhost:8000.

### 4. Create a local admin account. 

    python manage.py createsuperuser


## Useful Commands
- Add package dependencies with `poetry add <package name>`
- Run tests with `pytest`.
- Open a python shell with `python manage.py shell`
- Delete your data with `python manage.py shell` or completely reset your database (including migrations) with `python manage.py reset_db`

## Contributing

If you would like to contribute to this repository, a couple of helpful steps:

### Install pre-commit

Installing pre-commit ensures your code is properly formatted before committing any code.

    pre-committ install

### Branch your code

Before you start work on an issue/feature, make sure your code base is up to date. If you are working off of a forked repository, make sure you have STL DSA's repo as a remote and fetch/pull from there. 

On the `main` branch:

    git pull

Now create a new branch and switch to it:

    git checkout -b <feature-name>

where `<feature-name>` is whatever you'd like to work on.

Write some code, and when you think it's in a good state, run `pytest` to make sure it doesnt break anything. You should also write and pass your own tests for your new feature. When your tests pass, you may `git commit` your code. If you're ready to share the state of your code with others, `git push` your code to GitHub for others to review or continue your work. If your feature is done and you think your code is ready for prime time, [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).