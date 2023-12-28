# Workload: Statefulset

## Testing two docker images

```bash
# Build the apps
docker build -t backend .
docker build -t frontend .

# Tag and publish to docker hub
docker tag backend darvein/bapp:v1
docker tag frontend darvein/fapp:v1

docker push darvein/bapp:v1
docker push darvein/fapp:v1
```

## Deploy both apps in k8s

First create the SQL file as configmap:
```bash
k create configmap mysql-initdb-config --from-file=init-db.sql

# Create the Mysql service
k apply -f mysql.yml
k apply -f backend.yml
k apply -f frontend.yml
```


