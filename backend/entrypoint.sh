#!/bin/bash


python manage.py makemigrations

python manage.py migrate

echo "Creating superuser $DJANGO_SUPERUSER_EMAIL with username $DJANGO_SUPERUSER_USERNAME"

python manage.py createsuperuser --noinput

exec "$@"