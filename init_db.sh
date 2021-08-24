#!/bin/bash

if [ "$DJANGO_CONFIGURATION" == "Docker" ]; then
    python manage.py migrate
    python manage.py seed-db
fi

python manage.py runserver 0.0.0.0:8000