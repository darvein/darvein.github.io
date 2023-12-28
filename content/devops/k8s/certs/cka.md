# Certified Kubernetes Administrator

This is for EKS 1.22

## Kubernetes basics

### Controle plane

- Multiple servers
- Control the cluster
- Components:
  - kube-api-server: kubernetes API
  - etcd: key-value storage for cluster info
  - kube-scheduler: select available node to put a pod
  - kube-controller-manager: multiple utilities that automate tasks
  - cloud-controller-manager: only with aws, azure, gcp

### Nodes

- Components:
  - kubelete: communicates with control plane
  - container runtime: software to run containers
  - kube-proxy: networking between containers

## Building a kubernetes cluster

- 3 nodes minimum
- make sure have host names and all 3 nodes can ping each other by names
- /etc/modules-load.d/containerd.conf
  - add: overlay and br_netfilter
  - sudo modprobe
- /etc/sysctl.d/99-ubernetes-cri.conf
  - net.bridge.bridge-nf-call-iptables = 1
  - net.ip4.ip_forward = 1
  - net.bridge.bridge-nf-call-ip6tables = 1
  - sudo systemctl reload
- install containerd package
- /etc/containerd/config.toml
- systemctl restart containerd
- sudo swapoff -a and /etc/fstab disable swap
- install apt-transport-https curl
- curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add-
- apt-get install kubelet kubeadm kubectl
- apt-mark hold kubelet kubeadm kubectl
- (master) kubeadm init --por-network-cidr 192.168.0.0/16 --kubernetes-version 1.22.0
- (master): mkdir $HOME/.kube; cp -i /etc/kubernetes/admin.conf $HOME/.kube/config; chown $(id -u):$(id -g) $HOME/.kube/config
- (master): kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
- (master): kubeadm token create --print-join-command
- (node): kubeadm join $IPADDR --token $TOKEM --discovery-token-ca-cert-hash sha256:xxxxxx

## Namespaces

Virtual clusters on same cluster

## Tools

- kubeadm
- kubectl
- kompose
- kustomize
- minikube
- helm

## Safely draining a k8s node

- `kubectl drain $NODE_NAME --ignore-daemonsets --force` to remove node from the cluster
- `kubectl uncordon $NODE_NAME` to attach the node again to the cluster, enable k8s scheduler in the node

## Upgrade k8s with kubeadm

On the master node (control plane)
- kubectl drain k8s-control  --ignore-daemonsets
- sudo apt-get update && sudo apt install kubeadm
- sudo kubeadm upgrade plan v1.22.2
- sudo kubeadm upgrade apply v1.22.2
- sudo apt-get update && sudo apt install kubectl
- sudo systemctl daemon-reload
- sudo systemctl restart kubelet
- kubectl uncordon k8s-control

On workers:
- kubectl drain k8s-worker1 --ignore-daemonsets --force # from master
- sudo apt-get update && sudo apt install kubeadm
- sudo kubeadm upgrade node
- sudo apt-get update && sudo apt install kubectl
- sudo systemctl daemon-reload
- sudo systemctl restart kubelet
- kubectl uncordon k8s-worker1 # from master

## Backup and restore etcd

- `ETCDCTL_API=3 etcdctl --endopints $ENDPOINT snapshot save <file name>`
- `ETCDCTL_API=3 etcdctl --endopints $ENDPOINT snapshot restore <file name>`
