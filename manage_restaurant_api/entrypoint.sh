#!/bin/ash
SUPERUSER_NAME=${SUPERUSER_NAME}
SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD}

echo "Apply database migrations"
python manage.py migrate 
python manage.py collectstatic --noinput
python manage.py shell < createsuperuser.py

exec "$@"