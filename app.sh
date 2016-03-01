#!/bin/bash
python manage.py collectstatic --noinput  # Collect static files

exec gunicorn project.wsgi:application \
    --name liquorpark \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --access-logfile - \
    --log-file -