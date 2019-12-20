#!/bin/bash
./wait-for-it.sh postgres_db:5432 -- pipenv run python manage.py runserver 0.0.0.0:8080
