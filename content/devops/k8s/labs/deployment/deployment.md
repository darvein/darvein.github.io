# Workload: Deployment

## Testing two docker images

```bash
# Build the apps
~➤ docker build -t backend .
~➤ docker build -t frontend .

# Run the apps
~z➤ docker network create dummy
~z➤ docker run --network dummy -p 3000:3000 --name backend backend

# Tag and publish to docker hub
docker tag backend darvein/bapp:v1
docker tag frontend darvein/fapp:v1

docker push darvein/bapp:v1
docker push darvein/fapp:v1
```

## Deploy both apps in k8s

```bash
~z➤ kubectl apply -f backend.yml
deployment.apps/backend-deployment created
service/backend-service created

~z➤ kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
backend-deployment-5748f7d89f-27kxd   1/1     Running   0          2m24s
backend-deployment-5748f7d89f-6rc6l   1/1     Running   0          2m24s

# Repeat the same for frontend.yml
```

Accessing frontend app. Notice the service is being exposed on port 31000 (30000-32767 is a valid range).

You can find the minikube ip via: `minikube ip`

How to rollout undo?:
```bash
kubectl rollout undo deployment/frontend-deployment
kubectl rollout undo deployment/backend-deployment
```
