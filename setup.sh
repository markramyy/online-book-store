#!/bin/bash

printf "Generating Password to use...\n"

openssl rand -base64 24 | tr -d '=+/' | cut -c1-32
openssl rand -base64 24 | tr -d '=+/' | cut -c1-32


printf "Setting up Django project...\n"

python manage.py makemigrations
python manage.py migrate
python manage.py load_mock
python manage.py runserver
