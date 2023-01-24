# St. Louis DSA Website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/stldsa/site)

Welcome to the codebase for the St Louis DSA website! We hope this guide will make it easy for newcomers to get set up and contribute to website features.

## Quickstart

The quickest and easiest way to get plugged into our development environment is with VS Code Dev Containers. If you'd like to try out a different IDE, you may try either tunneling into the docker container created by `.devcontainer/docker-compose.yaml` or by installing the Python, Poetry, and Postgres dependencies yourself.  

### Creating and developing in your Dev Container

Click the "Devcontainers: Open" badge at the top of this README. Wait a few minutes while dependencies are installed and the database is initialized.

After a few minutes, you will see a prompt for an email address. Enter any email address (it doesn't have to be one you own; it can be a fake one like admin@example.com). Then, enter a password to create a superuser account for your local environment. You should then see the success message at the bottom of the terminal:

```bash
Done. Press any key to close the terminal.
```

Press any key and a new terminal shell will open. 

Run the following two commands to view a local copy of the site in your browser:

#### Activate your Python virtual environment
```bash
poetry shell
``` 

#### Run the web server:
```bash
python manage.py runserver
```

### More useful commands

Run the following commands to perform common web development tasks. If you're new to web development and/or Python and Django, understanding what these commands do is a good place to start learning.

#### Run tests
```bash
pytest
```

#### Make/run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Open a Python shell

```bash
python manage.py shell
```

### Add or remove packages with Poetry

```bash
poetry add requests
poetry remove requests
```

## Stack details

### Django

Right now, our website is primarily built using Python, particularly the Django web development framework. If you would like to develop tools using a different language or framework, please reach out to tech@stldsa.org and set up a meeting with a Tech Committee Chair so we can help you get started.

### Learning about Django

 If you'd like to learn the basics of Django, their [official tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) is excellent.

## Wagtail (CMS)

Many pages on our site are built with Wagtail, which is a nice Django-based content management system (CMS) designed to make it easier for non-programmers to update content on the site - read about the [Zen of Wagtail](https://docs.wagtail.io/en/stable/getting_started/the_zen_of_wagtail.html) to get the idea.

### Browse Wagtail

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
