git pull
docker-compose exec api pip install -r requirements.txt
docker-compose restart api
docker-compose ps