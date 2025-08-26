pip freeze > requirements
chmod +x ./entrypoint.sh


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

docker network rm manage_restaurant_api_rest_default

# effacer les volumes et container
# Arrêter et supprimer tous les conteneurs
docker compose down --volumes --remove-orphans

# Supprimer les réseaux non utilisés
docker network prune -f

# Supprimer les volumes non utilisés
docker volume prune -f

# Supprimer les conteneurs en cache
docker rm -f $(docker ps -aq) 2>/dev/null || true

# Relancer
docker compose up --build

alias dcl='docker compose -f docker-compose.yml'
# arreter
dcl down
# mettre à jour 
dcl up -d --build
# démarrer
dcl up -d

sudo netstat -tulnp | grep :80
sudo systemctl stop nginx
sudo systemctl disable nginx



