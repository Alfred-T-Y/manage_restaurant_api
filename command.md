pip freeze > requirements
chmod +x ./entrypoint.sh
docker-compose up -d --build
docker-compose down

# Supprime la base de données (par exemple db.sqlite3 ou reset la DB PostgreSQL)
rm db.sqlite3  # si SQLite

# Supprime les fichiers de migration
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recrée les migrations
python manage.py makemigrations
python manage.py migrate

# accéder au shell du container django
docker exec -it django_manage_restaurant /bin/sh

# lance redis
redis-server       
# lance django
python manage.py runserver   
# lance celery worker
celery -A manage_restaurant_api worker --loglevel=info 

sudo ss -tulnp | grep 6379

daphne manage_restaurant_api.asgi:application

git pull origin main

docker-compose -f docker-compose.yml up -d --build
