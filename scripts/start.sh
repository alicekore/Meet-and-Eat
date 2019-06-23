#!/usr/bin/env bash
export DECOUPLE_CONFIGURATION=production;
python manage.py collectstatic --no-input;
python manage.py makemigrations;python manage.py migrate;
gunicorn meeteat.wsgi -b 0.0.0.0:8000;
