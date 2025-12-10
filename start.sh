#!/usr/bin/env bash
source ../venv/bin/activate
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
gunicorn dreamPC2.wsgi:application --bind 0.0.0.0:$PORT