#!/bin/bash
export DJANGODIR=/home/username/SafeLab
export DJANGO_SETTINGS_MODULE=config.settings

cd $DJANGODIR

source $DJANGODIR/.venv/bin/activate

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3