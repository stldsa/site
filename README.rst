STL DSA
=======

Website for the St Louis chapter of the Democratic Socialists of America

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT



Docker Setup
------------
To set up your environment using Docker, run:
  ``docker-compose up``

this will build your container, install your dependencies, and run services for your database and web server.

To execute a command in your container's environment, prefix your commands with ``docker-compose run web <your command here>``.  

To get our application working, we need to initialize our database:
``docker-compose run web python manage.py migrate``

and seed it with fake data:
  ``docker-compose run web python manage.py seed-db``
  
You should now be able to view a functional copy of the website in your browser at ``http://localhost:8000``.

Manual Setup
------------

Prerequisites
^^^^^^^^^^^^^
* python 3.8.5 (I suggest pyenv to manage python versions)
* poetry_ dependency manager
* postgresql

.. _poetry: https://python-poetry.org/docs/#installation

Setting Up Your Local Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``poetry shell`` to open your virtual environment shell
* ``poetry install`` to install dependencies within virtual Environment

Initialize Database
^^^^^^^^^^^^^^^^^^^
* ``python manage.py makemigrations``

Run dev server
^^^^^^^^^^^^^^

* ``python manage.py runserver``

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser


Running tests with pytest
~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Wagtail CMS
--------------
A good portion of the site is built using Wagtail - read about the `Zen of Wagtail https://docs.wagtail.io/en/stable/getting_started/the_zen_of_wagtail.html`_ to get the idea. Go to ``http://locahost:8000/cms`` with a superuser account to log in and poke around. 