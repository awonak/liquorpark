#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec gunicorn project.wsgi:application \
    --name liquorpark \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --access-logfile - \
    --log-file -
