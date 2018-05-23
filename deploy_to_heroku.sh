#!/usr/bin/env bash
git pull origin
python manage.py makemigrations
git add -f */migrations/*
git commit -m "add migrations for heroku"
git push heroku
heroku run python manage.py migrate
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
git commit -m "removed migrations files"