#!/bin/bash

if [ "$DJANGO_CONFIGURATION" == "Docker" ]; then
    python manage.py migrate
    python manage.py seed-db
    python manage.py createsuperuser --noinput
    python manage.py autopopulate_main_menus
    sass --watch /app/stl_dsa/static/sass:/app/stl_dsa/static/css & 
fi

python manage.py runserver 0.0.0.0:8000