pip freeze > requirements
chmod +x ./entrypoint.sh
docker-compose up -d --build
docker-compose down