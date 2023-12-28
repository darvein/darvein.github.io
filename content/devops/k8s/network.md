# Network, Ingress, Services, etc

# Content

- [Network, Ingress, Services, etc](#network-ingress-services-etc)
- [Content](#content)
    - [Pods Networking](#pods-networking)
        - [Network policies for Pods:](#network-policies-for-pods)
    - [DNS](#dns)
    - [Services](#services)
    - [Ingress](#ingress)
    - [Gateway API](#gateway-api)

## Pods Networking
We can bootstrap kuberentes via minikube with these configs:
```bash
minikube start \
   --memory=8192 --cpus=4 \
   --nodes=3 \
   --driver=virtualbox \
   --network-plugin=cni --cni=calico \
   --feature-gates=JobPodFailurePolicy=true,PodDisruptionConditions=true \
   --insecure-registry "registry.local:5000" \
   --container-runtime=docker \
   --service-cluster-ip-range=10.96.0.0/12 \
   --extra-config=controller-manager.cluster-cidr=10.244.0.0/16 \
   --extra-config=controller-manager.node-cidr-mask-size-ipv4=24
```
Highlights:
- `cluster-cidr`: CIDR where pods will be deployed
- `service-cluster-ip-range`: ClusterIP for services

Kube-proxy on each node receives traffic from the service-cluster-ip-range and forwards to the backend pods.

You can verify the network setup:
- Check the cluster service ip range: `kubectl cluster-info dump | grep -m 1 service-cluster-ip-range`
- Check pods ip range: `kubectl cluster-info dump | grep -m 1 cluster-cidr`
- Verify each node cidr: `kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}' `

### Network policies for Pods:
By default pods have no restrictions:
 
What can be filtered in a network policy: 
- Entites: 
    - Pod
    - Namespace
    - ipBlock
- Isolation modes: 
    - Ingress
    - Egress

## DNS
Pods and services get an entry en DNS Service
pod-ip-address.my-namespace.pod.cluster-domain.example.
A pod can have a hostname and subdomain

Once pods are behind a service, both the service and pods have are registered into coredns service:
```bash
kubectl exec -it busybox1 -- nslookup busybox-2.busybox-subdomain.default.svc.cluster.local
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      busybox-2.busybox-subdomain.default.svc.cluster.local
Address 1: 10.244.205.199 busybox-2.busybox-subdomain.default.svc.cluster.local
```

Pods can have custom DNS config:
```yaml
  dnsPolicy: ClusterFirstWithHostNet
```
Where the policy can be:
- Default: host node dns resolver to pods
- ClusterFirst: upstream dns resolver
- ClusterFirstWithHostNet: first cluster, then host of the pod
 
Or you can manually specify the DNS config:
```yaml
apiVersion: v1
kind: Pod
metadata:
  namespace: default
  name: dns-example
spec:
  containers:
    - name: test
      image: nginx
  dnsPolicy: "None"
  dnsConfig:
    nameservers:
      - 192.0.2.1 # this is an example
    searches:
      - ns1.svc.cluster-domain.example
      - my.dns.search.suffix
    options:
      - name: ndots
        value: "2"
      - name: edns0
```

## Services
A service can expose a set of Pods via Endpoints which are the entitities where the traffic is going to be forwareded.

Each pod have a unique cluster-wide IP.

Via services we can expose a set of pods via Endpoints.


```bash
~z➤ k get svc
NAME                TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
busybox-subdomain   ClusterIP   None         <none>        1234/TCP   44m
kubernetes          ClusterIP   10.96.0.1    <none>        443/TCP    75m
```

Endpoints
```bash
~z➤ k get endpointslices.discovery.k8s.io
busybox-subdomain-mngmj   IPv4          1234    10.244.205.199,10.244.151.3   44m

~z➤ k get endpoints
busybox-subdomain   10.244.151.3:1234,10.244.205.199:1234   44m
```

If the service doesn’t have any label then the EndpointSlice is not created nor Endpoints.
The service allows you to create multiport configuration
 
In case we need a Service with no labels and point the service to an external service outside the cluster maybe. Then create an EndpointSlice.
 
***How we expose a Service***
- ClusterIP (default): it allocates a cluster-wide IP Addr for internal access. If we want to expose it outside the cluster we have to use Ingress or Gateway API. If we put ClusterIP to None, it becomes headless, no access. Ip comes from —service-cluster-ip-range value.
- NodePort: It opens a port on every node and it forward the traffic to the right ports. Ports are picked from range 30000-32767, you can also manually specify a port on that range.
- LoadBalancer: Kubernetes can communicate with an external LB and configure it. A LB can also work internally, balance traffic just internally.
- ExternalName: We use a Service and the backend will be an external service, the name fqdn is needed so k8s can configure its internal DNS Service. For example service my-service.prod.svc.cluster.local will be redirected to www.example.com it works at DNS level.

A service can have an specific ip address to receive traffic via prop: externalIPs

Service can also route traffic internally ,meaning route the traffic to the pod’s host where the initial traffic originated.

## Ingress

It can expose a service outside the cluster and also manage the SSL/TLS Terminations. It has a managed-lb. 
The ingress needs to be installed in k8s, and it will come with an Ingress Controller.
An ingress can route traffic based on hosts and paths. 
Hostnames can be wildcards. Paths can have regex “exact” or “prefix”.

An ingressClass is needed so it can manage the external LB and routing via ingressClass. This ingressClass can be cluster-wide or namespaces during installation via YAML.

Same as storageClass default, we can specify an ingresClass as default:   
annotations: `ingressclass.kubernetes.io/is-default-class: "true"`

Resource Backend, so Ingress can expose a static content bucket.
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-resource-backend
spec:
  defaultBackend:
    resource:
      apiGroup: k8s.example.com
      kind: StorageBucket
      name: static-assets
  rules:
    - http:
        paths:
          - path: /icons
            pathType: ImplementationSpecific
            backend:
              resource:
                apiGroup: k8s.example.com
                kind: StorageBucket
                name: icon-assets
```

Sample ingress TLS
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: testsecret-tls
  namespace: default
data:
  tls.crt: base64 encoded cert
  tls.key: base64 encoded key
type: kubernetes.io/tls
 
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-example-ingress
spec:
  tls:
  - hosts:
      - https-example.foo.com
    secretName: testsecret-tls
  rules:
  - host: https-example.foo.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
```
 
## Gateway API
Similar to Ingress.
 
It requires a class first
```yaml
---
-- Gateway Class
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: example-class
spec:
  controllerName: example.com/gateway-controller

---
-- Then we define the gateway
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: example-gateway
spec:
  gatewayClassName: example-class
  listeners:
  - name: http
    protocol: HTTP
    port: 80

---
#Then we specify the rules http
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: example-httproute
spec:
  parentRefs:
  - name: example-gateway
  hostnames:
  - www.example.com
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /login
    backendRefs:
    - name: example-svc
      port: 8080
```
