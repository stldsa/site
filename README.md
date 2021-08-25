# St. Louis DSA Website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the codebase for the St Louis DSA website! We hope this guide will make it easy for newcomers to get set up and contribute to website features.

## Before You Begin

Right now, our website is primarily built using Python, particularly the Django web development framework. If you would like to develop tools using a different language or framework, please reach out to tech@stldsa.org and set up a meeting with a Tech Committee Chair so we can help you get started.

### Learning about Django

 If you'd like to learn the basics of Django, their [official tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) is excellent.

### Wagtail CMS

Many pages on our site are built with Wagtail, which is a nice Django-based content management system (CMS) designed to make it easier for non-programmers to update content on the site - read about the [Zen of Wagtail](https://docs.wagtail.io/en/stable/getting_started/the_zen_of_wagtail.html) to get the idea.

## Getting Set Up

The easiest way to get started with your local development environment is through our Docker Setup, which is outlined below. If these instructions do not work (or if you'd like to set up your own environment and have questions), please reach out to tech@stldsa.org or [open a GitHub issue](https://github.com/stldsa/site/issues/new/choose).

### 1. Clone the repository

    $ git clone https://github.com/stldsa/site.git stldsa

If you are a member of DSA, ask to be added as a maintainer of the repo. If you are not a member, feel free to fork the repo. `cd stldsa` to move to the project root folder.

### 2. [Install Docker](https://docs.docker.com/engine/install/) (if you haven't already)

### 3. Build the Docker Image and create the Docker container

    $ docker-compose up

The first time you do this, Docker uses the Dockerfile to *build* an **image**, which is basically a static blueprint for a Docker container. This will take a few minutes and does things like set up the operating system and install package dependencies. Subsequent builds will run off a cache and should run faster. Then it *creates* a **container**, which you should think of as an ephemeral, modifiable instantiation of the image. Every time you create a container, you will begin with a fresh database (corollary: every time you remove a container, you destroy the database). 

Accordingly, avoid running `docker compose up` without first running `docker-compose down` (or otherwise removing the container). It shouldn't technically break anything if you do, but we want to avoid repeatedly attempting to initialize the database as good practice.

 After all of the scripts are done executing, visit http://localhost:8000 to view your local copy of the site. Magic!

Running  `docker-compose stop` simply stops running the container, freeing up memory and the `localhost:8000` port. Use `docker-compose start` to restart it.

You can also perform many of these tasks with the Docker extension for VS Code if you prefer using a GUI.

## Developing

You can open a bash shell inside the container with:

    $ docker-compose run web bash

and close the shell with `Ctrl+D`. Alternatively you can run one-off commands with `docker-compose exec web <command>`. You may want to create an alias such as `alias stldsa="docker-compose exec web"` that allows you to run commands with the much simpler `stldsa <command>`. Persist this alias across shell sessions by adding `>> ~/.bashrc` (Linux) or `>> ~/.bash_profile` (macOS) to the alias command.

## More useful commands

- Add package dependencies with `poetry add <package name>` (we use [poetry](https://python-poetry.org/) instead of `pip`). Note: may take a while to resolve dependencies first time you run this command.
- Run tests with `pytest`.
- Open a Python shell with `python manage.py shell`
- Delete your data (but not your [migrations](https://docs.djangoproject.com/en/3.2/topics/migrations/)) with `python manage.py flush` and restore seed data with `python manage.py seed-db`.

## Browse the Wagtail CMS

The startup scripts create an admin user with the email *admin@example.com* and the password *password*.  Go to http://localhost:8000/cms and enter these credentials to open the Wagtail admin interface. Browse around and get a sense for the site tree. Notice that upon returning to the "front end" of the website, you can view a shortcut to some convenient options in the lower-right corner of pages that use Wagtail.

## Contributing

If you would like to contribute to this repository, a couple of helpful steps:

### Code formatting

Use [black](https://github.com/psf/black) in your IDE to automatically format your code according to the project standards each time you save your code. Black automatically comes with the Python extension for VS Code and should come preconfigured according to the `.vscode` configuration file that comes with this repo. Installing **pre-commit** ensures your code is black-formatted before committing any code:

    pre-committ install

### Working on branches

Before you start work on an issue/feature, make sure your code base is up to date. 

On the `main` branch:

    git pull

If you are working off of a forked repository, make sure you have STL DSA's repo as a remote and pull from there, i.e. `git pull <remote>`. 

Now create a new branch and switch to it:

    git checkout -b <feature-name>

where `<feature-name>` is whatever you'd like to work on.

Write some code, ideally with some tests. Commit frequently as you go, running tests with `pytest` to make sure it doesnt break anything before each commit. When you're ready to share the state of your code with others, `git push` your feature branch to GitHub for others to review or continue your work. If your feature is complete and you think your code is ready for prime time, [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) on the `main` branch.
