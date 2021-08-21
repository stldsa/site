# St. Louis DSA Website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the website for the St Louis chapter of the Democratic Socialists of America! We hope this guide will make it easy for newcomers to contribute to website features.

## Before You Begin

Right now, our website is primarily built using Python, particularly the Django web development framework. If you would like to contribute to tools using a different language or framework, please reach out to tech@stldsa.org and set up a meeting with a Tech Committee Chair so we can help you get started.

### Learning about Django

Our site is built on Django, a powerful Python web development framework. If you'd like to learn the basics of Django, their [official tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) is excellent.

### Wagtail CMS

Many pages on our site are built with Wagtail, which is a nice little Django-based CMS backend to make it easier for non-programmers to update content on the site - read about the [Zen of Wagtail](https://docs.wagtail.io/en/stable/getting_started/the_zen_of_wagtail.html) to get the idea.

## Getting Set Up

The easiest way to get started with your local development environment is through our Docker Setup, which is outlined below. If these instructions do not work (or if you'd like to set up your own environment and have questions), please reach out to tech@stldsa.org or make a pull request with suggested changes.

### Suggestions for Windows Users

- Using [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) (WSL) will make your life easier for many common console commands and environment details.
- [VS Code](https://code.visualstudio.com/) is a code editor that has good support for WSL.

### Docker Setup

1. If you have not already, download and install [Docker Desktop](https://www.docker.com/get-started).

   -If you're using WSL, install Docker Desktop for Windows and follow the post-installation instructions [here](https://docs.docker.com/desktop/windows/wsl/#install).

2. Run `docker-compose up`. This will build your Docker image (if it has not already been built), install all dependencies, and spin up a container with services for your database and web server. Your console window will show output for these services. Open a new console window to continue.

3. Create an alias for running commands in your docker container using our setup.

   - WSL (bash) : `echo 'function stldsa() { docker-compose run web "$@"; }' >> ~/.bashrc`
   - macOS (Terminal) : `echo 'function stldsa() { docker-compose run web "$@"; }' >> ~/.bash_profile`

   To run a command inside the docker container, you may now simply type `stldsa <command>`.

4. To get our application working, we need to initialize our database with something called a migration. Run `stldsa python manage.py migrate`.

5. Now our website needs some fake data to render properly. Seed the database with `stldsa python manage.py seed-db`. You should now be able to view a functional copy of the website in your browser at http://localhost:8000.

6. Create a local admin account. Run `stldsa python manage.py createsuperuser` and follow the instructions.

When you are done with your session, you may run `docker-compose stop` (or Ctrl+C in your console window running the container) to stop running the containers and free up some memory. Running `docker-compose down` will stop the containers and remove them -- essentially deleting any data you may have added. If you'd like to make changes to the database that can easily be redeployed, consider contributing to the db-seed command.

## Basic Commands

- Run tests with `stldsa pytest`.
- Open a command shell with `stldsa python manage.py shell`

## Contributing

TODO
