# Deployment - local


```shell
docker compose -f deployment/local/docker-compose.yml stop
docker compose -f deployment/local/docker-compose.yml build
docker compose -f deployment/local/docker-compose.yml up --detach
```