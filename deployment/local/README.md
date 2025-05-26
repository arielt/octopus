# Deployment - local

## Docker compose
```shell
docker compose -f deployment/local/docker-compose.yml stop

# removes containers, networks
# docker compose -f deployment/local/docker-compose.yml down

docker compose -f deployment/local/docker-compose.yml build
docker compose -f deployment/local/docker-compose.yml up --detach
```

## Vault
Init: [http://0.0.0.0:8200/](http://0.0.0.0:8200/)

```shell
# access container
docker exec -it local-vault-1 /bin/sh
docker logs local-vault-1

# mount kv2 secret engine
docker exec local-vault-1 vault login <token>
docker exec local-vault-1 vault secrets enable -path secret kv-v2
docker exec local-vault-1 vault secrets list
```

Sample operations
```shell
docker exec local-vault-1 vault status
docker exec local-vault-1 vault login <token>
docker exec local-vault-1 vault kv put /secret/octopus password=pass
docker exec local-vault-1 vault kv get /secret/octopus
```
