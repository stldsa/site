#!/bin/bash

if [ "$DJANGO_CONFIGURATION" == "Docker" ]; then
    python manage.py migrate
    python manage.py seed-db
    python manage.py createsuperuser --noinput
    python manage.py autopopulate_main_menus
fi
