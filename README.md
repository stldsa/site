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

 This command builds **images** for both your database container (from the standard DockerHub postgres repository) and your web service container (from the Dockerfile). These images essentially provide a starting point for Docker containers to run off of so that they can be quick and painless. Thus, building them will take a few minutes the first time while it does things like set up the operating system and install package dependencies. Subsequent builds will use a cache and should execute faster - you should only have to rebuild if you make changes to the Dockerfile or need to install a new Python package. 

### 4. Create and run the service containers

    $ docker-compose up

 This creates two **containers** (again, one for the database and one for the web service), which are designed to be ephemeral, modifiable instantiations of the images. Using `up` also executes the final `CMD` step in the Dockerfile (which in our case, runs a bash script to initialize the database). Lastly, it keeps the services running so that a) the web service can access the database and b) and we can access the web server in our browser at [localhost:8000](http://localhost:8000). Go ahead and check it out! Magic!
 
 When you are done using the browser, you can run `docker-compose stop` if you want to stop the services, which will free up port 8000 and some memory. `docker-compose start` will spin it back up again. Run `docker-compose down` to stop *and* delete the containers (including the database). Or just keep it running forever 🤷

If you're using [VS Code](https://code.visualstudio.com/) as your IDE, you can also perform many of these tasks with the Docker extension whenever you might prefer using a GUI.

## Developing

Most commands that you'll need to run on a regular basis you should perform in a new container:

    $ docker-compose run --rm web <command>

The `--rm` flag is optional and deletes your containers after they stop, which will prevent your hard drive from cluttering up with containers. If at some point you end up with a lot of empty containers anyways, just run `docker container prune`.

In contrast to `up`, `run` overwrites the `CMD` step with your arguments, so the database initialization script is skipped.

> Tip: You may want to append an alias function in your `.bashrc` (Linux/Ubuntu) or `.bash_profile` (macOS) using `echo 'function stldsa() { docker-compose run web "$@"; }' >> ~/.bashrc`. This will allow you to run commands with the much simpler `stldsa <command>`.

## Common/useful commands

- Open bash shells inside the container with:

      $ docker-compose run web bash

    Run your commands and close the bash shell with `Ctrl+D`. This might be useful for installing new dependencies without needing to rebuild the Docker image. To keep things clean, try to avoid using the bash shell unless you explicitly need to run multiple terminal commands.

    > Note: Due to some quirks in the way Docker manages virtual environments, you should use `pip` inside the container when updating dependencies, even though the project uses [Poetry](https://python-poetry.org/) outside of Docker.

- Open Python shells with:

      $ docker-compose run web python manage.py shell

- Run tests:

      $ docker-compose run web pytest

- When you change any model fields, you must make some new migrations:

      $ docker-compose run web python manage.py makemigrations
      $ docker-compose run web python manage.py migrate

## Browse Wagtail CMS

The startup scripts create an admin user with the email *admin@example.com* and the password *admin1234* (You can [override these settings](https://docs.djangoproject.com/en/3.0/ref/django-admin/#createsuperuser) using your environment variables).  Go to http://localhost:8000/cms and enter these credentials to open the Wagtail admin interface. Browse around, navigate the site tree, and try making a page yourself! Notice that upon returning to the "front end" of the website, if you're viewing a page that uses Wagtail (which is most of them), you can now see a nifty shortcut the lower-right corner.

## Contributing

If you would like to contribute to this repository, a couple of helpful steps:

### Code formatting

Use [Black](https://github.com/psf/black) in your IDE to automatically format your code according to Black's strict standards each time you save your code. Black automatically comes with the Python extension for VS Code and should come preconfigured according to the `.vscode` file that comes with this repo. 

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