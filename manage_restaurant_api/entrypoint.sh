#!/bin/ash

echo "Apply database migrations"
python manage.py migrate 
python manage.py collectstatic --noinput
python manage.py shell < createsuperuser.py

exec "$@"