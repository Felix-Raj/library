#!/usr/bin/env bash
git add -f */migrations/*
git commit -m "add migrations for heroku"
git push heroku
heroku run python manage.py migrate