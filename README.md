# St. Louis DSA Website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the codebase for the St Louis DSA website! We hope this guide will make it easy for newcomers to get set up and contribute to website features.

## Quickstart

If you know what you're doing and ready to jump in:

    $ docker-compose up

## Before You Begin

Right now, our website is primarily built using Python, particularly the Django web development framework. If you would like to develop tools using a different language or framework, please reach out to tech@stldsa.org and set up a meeting with a Tech Committee Chair so we can help you get started.

### Learning about Django

 If you'd like to learn the basics of Django, their [official tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) is excellent.

### Wagtail CMS

Many pages on our site are built with Wagtail, which is a nice Django-based content management system (CMS) designed to make it easier for non-programmers to update content on the site - read about the [Zen of Wagtail](https://docs.wagtail.io/en/stable/getting_started/the_zen_of_wagtail.html) to get the idea.

## Getting Set Up

The easiest way to get started with your local development environment is through our Docker Setup, which is outlined below. If these instructions do not work (or if you'd like to set up your own environment and have questions), please reach out to tech@stldsa.org or [open a GitHub issue](https://github.com/stldsa/site/issues/new/choose).

> Tip: The commands in this guide assume you are using a UNIX shell, i.e. on macOS or Ubuntu. If you're a Windows user, you might be able to get by with Git Bash (which comes with [Git for Windows](https://gitforwindows.org/)) or [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 

### 1. Clone the repository

    $ git clone https://github.com/stldsa/site.git stldsa && cd stldsa

If you are a member of DSA, ask to be added as a maintainer of the repo. If you are not a member, feel free to fork the repo.

### 2. [Install Docker](https://docs.docker.com/engine/install/) (if you haven't already)

### 3. Build the Docker Image

    $ docker-compose build

 This command builds **images** for both your database container (from the standard DockerHub postgres repository) and your web service container (from the Dockerfile). These images essentially provide a starting point for Docker containers to run off of so that they can be quick and painless. Thus, building them will take a few minutes the first time while it does things like set up the operating system and install package dependencies. Subsequent builds will use a cache and should execute faster - you should only have to rebuild if you make changes to the Dockerfile. 

### 4. Create and run the service containers

    $ docker-compose up

 This creates two **containers** (again, one for the database and one for the web service), which are designed to be ephemeral, modifiable instantiations of the images. It also contains an additional temporary container to run database integrations using the `init-db.sh` script. The web and database containers will keep running so that a) the web service can access the database and b) and we can access the web server in our browser at [localhost:8000](http://localhost:8000). Go ahead and check it out! Magic!
 
 When you are done using the browser, you can run `docker-compose stop` if you want to stop the services, which will free up port 8000 and some memory. `docker-compose start` will spin it back up again. Run `docker-compose down` to stop *and* delete the containers (which will also delete the database). Or just keep it running forever! 🤷

If you're using [VS Code](https://code.visualstudio.com/) as your IDE, you can also perform many of these tasks with the Docker extension whenever you might prefer using a GUI. Additionally the repo includes a `.devcontainer` settings folder so you can try out VS Code's Development Containers feature, though developing in this environment hasn't been fully tested.

## Developing

Most commands that you'll need to run on a regular basis you should perform in a new container:

    $ docker-compose run django <command>

> Tip: You may want to append an alias function in your `.bashrc` / `.bash_profile`:

Linux/Ubuntu:

     $ echo 'function stldsa() { docker-compose run django "$@"; }' >> ~/.bashrc` 

macOS:    

     $ echo 'function stldsa() { docker-compose run django "$@"; }' >> ~/.bash_profile`

This will allow you to run commands with the much simpler `stldsa <command>`.

**The rest of this guide uses the `stldsa` alias as described in the above tip**

## More common/useful commands

- Open bash shells inside the container with:

      $ stldsa bash

- Open python shells inside the container with

      $ stldsa python manage.py shell

- Add dependencies from the Python Package Index with

      $ poetry add <package>
        
 You may need to rebuild your Docker images with `docker-compose build`.
        
- Run tests:

      $ stldsa pytest

- When you change any model fields, you must make some new migrations:

      $ stldsa python manage.py makemigrations
      $ stldsa python manage.py migrate

<!-- - Re-seed your database:

      $ stldsa python manage.py flush
      $ stldsa python manage.py seed-db -->

- More helpful aliases:

      $ echo 'function stldsa-manage() { stldsa python manage.py "$@"; }' >> ~/.bashrc
      $ echo 'function docker-reset() { docker-compose down && docker-compose up; }' >> ~/.bashrc

## Browse Wagtail CMS

The startup scripts create an admin user with the email `admin@example.com` and the password `stldsa` (You can [override these settings](https://docs.djangoproject.com/en/3.0/ref/django-admin/#createsuperuser) using your environment variables if you really want to).  Go to http://localhost:8000/cms and enter these credentials to open the Wagtail admin interface. Browse around, navigate the site tree, and try making a page yourself! Notice that upon returning to the "front end" of the website, if you're viewing a page that uses Wagtail (which is most of them), you can now see a nifty shortcut icon the lower-right corner.

## Contributing

If you would like to contribute to this repository, a couple of helpful steps:

### Code formatting

Use [Black](https://github.com/psf/black) in your IDE to automatically format your code according to Black's strict linting standards each time you save your code. Black automatically comes with the Python extension for VS Code and should come preconfigured according to the `.vscode` file that comes with this repo. 

> *Optional*: Install **pre-commit** to ensure your code is black-formatted before each of your commits (this should be redundant assuming you're already running Black in the first place):

    pre-committ install

### Working on branches

Before you start work on an issue/feature, make sure your code base is up to date. 

On the `main` branch:

    $ git pull

If you are working off of a fork, make sure you have STL DSA's repo as a remote repo and pull from there, i.e. `git pull <remote>`. 

Now create a new branch and switch to it:

    $ git checkout -b <feature-name>

where `<feature-name>` is whatever you'd like to work on.

Write some code, ideally with some tests. Commit frequently as you go, running tests with `pytest` to make sure it doesnt break anything before each commit. When you're ready to share the state of your code with others, push your **feature branch** to GitHub for others to review or continue your work. You can't push to `main` so don't even try!

     $ git push <feature-branch>

If your feature is complete and you think your code is ready for prime time, [open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) on the `main` branch.

Happy coding!
