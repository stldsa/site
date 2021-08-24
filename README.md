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

    git clone https://github.com/stldsa/site.git

If you are a member of DSA, ask to be added as a maintainer of the repo. If you are not a member, feel free to fork the repo.

### 2. [Install Docker](https://docs.docker.com/engine/install/) (if you haven't already)

### 3. Spin up a Docker Container

    docker-compose up -d
    
The first time you run this command builds the Docker *image* the container is based on. The `-d` flag runs the container in 'detached' mode so you can continue using the same terminal. If you'd like to see the console logs from the running services, omit it.

### 4. Initialize your Database

1. Open a bash shell inside the container:

       docker-compose run web bash

2. Run your initial [migration](https://docs.djangoproject.com/en/3.2/topics/migrations/) to set up the database schema:

       python manage.py migrate

3. Now we need to seed our database with some fake data:

       python manage.py seed-db
      
 You should now be able to view a functional copy of the website in your browser at http://localhost:8000. 
 
4. Create a local admin account. 

       python manage.py createsuperuser


You're all set up! You can close out of the container shell with `Ctrl+D`. Reopen the shell at any time if you would like to develop inside the container, or run commands with `docker-compose run web <command>`, OR create an alias such as with `alias stldsa="docker-compose run web"`.


## Useful Commands
- Add package dependencies with `poetry add <package name>` (instead of using `pip`). Note: may take a while to resolve dependencies first time you run this command.
- Run tests with `pytest`.
- Open a Python shell with `python manage.py shell`
- Delete your data with `python manage.py flush` or completely reset your database (including migrations) with `python manage.py reset_db`.

## Contributing

If you would like to contribute to this repository, a couple of helpful steps:

### Code formatting

Use [black](https://github.com/psf/black) in your IDE to automatically format your code according to the project standards upon saving. Black automatically comes with the Python extension for VS Code and should come preconfigured according to the `.vscode` file that comes with this repo. Installing pre-commit ensures your code is properly formatted (using [black]) before committing any code.

    pre-committ install

### Working on branches

Before you start work on an issue/feature, make sure your code base is up to date. 

On the `main` branch:

    git pull

If you are working off of a forked repository, make sure you have STL DSA's repo as a remote and pull from there, i.e. `git pull <remote>`. 

Now create a new branch and switch to it:

    git checkout -b <feature-name>

where `<feature-name>` is whatever you'd like to work on.

Write some code, and ideally, some tests to go with it. Commit frequently as you go, running tests with `pytest` to make sure it doesnt break anything before each commit. When you're ready to share the state of your code with others, `git push` your commits to GitHub for others to review or continue your work. If your feature is complete and you think your code is ready for prime time, [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
