# Workload: Daemonset

## Deploying Resources

### Mysql
```bash
~z➤ k apply -f mysql.yml
configmap/sql-create created
secret/mysql-secret created
service/mysql-service created
statefulset.apps/mysql created
```

### Backend
```bash
~z➤ k apply -f backend.yml
deployment.apps/backend-deployment created
service/backend created

~z➤ k get pods
NAME                                  READY   STATUS     RESTARTS   AGE
backend-deployment-6b77dc6779-5rznl   0/1     Init:1/2   0          2s
mysql-0                               1/1     Running    0          2m22s

~z➤ k get pods
NAME                                  READY   STATUS    RESTARTS      AGE
backend-deployment-6b77dc6779-5rznl   1/1     Running   3 (33s ago)   3m8s
mysql-0                               1/1     Running   0             49s
```

### Frontend

```bash
~z➤ k apply -f frontend.yml
deployment.apps/frontend-deployment created
service/frontend created

~z➤ k get pods
NAME                                   READY   STATUS    RESTARTS   AGE
backend-deployment-7b55546f59-zdlff    1/1     Running   0          21m
frontend-deployment-66cd8c8b68-7ndl9   1/1     Running   0          9s
mysql-0                                1/1     Running   0          49m
```

### Prometheus

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/prometheus \
    --set server.service.type=NodePort \
    --version 25.1.0
kubectl get daemonsets
minikube service [service-name] --url

export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services prometheus-server)
export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
echo http://$NODE_IP:$NODE_PORT

helm uninstall prometheus
```

We can see the prometheus node_exporter has these configs, which makes sense as it requires elevated privileges to grab system info:
```bash
cat /proc/1/status
...
Uid:    0       0       0       0
Gid:    0       0       0       0
CapPrm: 000001ffffffffff
CapEff: 000001ffffffffff
CapBnd: 000001ffffffffff
...
```
#### Testing Prometheus
```bash
# cpu total usage
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100)

# mem usage
node_memory_MemTotal_bytes - node_memory_MemFree_bytes

# disk space used on root
node_filesystem_size_bytes{fstype!="",mountpoint="/"} - node_filesystem_free_bytes{fstype!="",mountpoint="/"}

# uptime
node_time_seconds - node_boot_time_seconds
```

### Daemonset demo
```bash
# Quick review into documentation
k explain daemonset.spec.template

~z➤ k apply -f dog-daemonset.yml
configmap/dog-script created
daemonset.apps/dog-daemonset created
```
