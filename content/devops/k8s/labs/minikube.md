# Installing minikube

Needed packages:
    - minikube: For installation follow instructions: https://minikube.sigs.k8s.io/docs/start/ - most package managers have a binary ready to be installed on your system.
    - vagrant

Star up k8s cluster with minikube:
```bash
➤ minikube start --driver=virtualbox
😄  minikube v1.31.2 on Arch
✨  Using the virtualbox driver based on user configuration
💿  Downloading VM boot image ...
E1005 17:51:25.025455    4640 iso.go:90] Unable to download https://storage.googleapis.com/minikube-builds/iso/16971/minikube-v1.31.0-amd64.iso: getter: &{Ctx:context.Background Src:https://storage.googleapis.com/minikube-builds/iso/16971/minikube-v1.31.0-amd64.iso?checksum=file:https://storage.googleapis.com/minikube-builds/iso/16971/minikube-v1.31.0-amd64.iso.sha256 Dst:/home/n0kt/.minikube/cache/iso/amd64/minikube-v1.31.0-amd64.iso.download Pwd: Mode:2 Umask:---------- Detectors:[0x55fe4cb8b640 0x55fe4cb8b640 0x55fe4cb8b640 0x55fe4cb8b640 0x55fe4cb8b640 0x55fe4cb8b640 0x55fe4cb8b640] Decompressors:map[bz2:0xc0005d3360 gz:0xc0005d3368 tar:0xc0005d3310 tar.bz2:0xc0005d3320 tar.gz:0xc0005d3330 tar.xz:0xc0005d3340 tar.zst:0xc0005d3350 tbz2:0xc0005d3320 tgz:0xc0005d3330 txz:0xc0005d3340 tzst:0xc0005d3350 xz:0xc0005d3370 zip:0xc0005d3380 zst:0xc0005d3378] Getters:map[file:0xc000902ed0 http:0xc0005ce2d0 https:0xc0005ce320] Dir:false ProgressListener:0x55fe4cb4bce0 Insecure:false DisableSymlinks:false Options:[0x55fe49eea1a0]}: invalid checksum: Error downloading checksum file: bad response code: 404
💿  Downloading VM boot image ...
    > minikube-v1.31.0-amd64.iso....:  65 B / 65 B [---------] 100.00% ? p/s 0s
    > minikube-v1.31.0-amd64.iso:  289.20 MiB / 289.20 MiB  100.00% 7.56 MiB p/
👍  Starting control plane node minikube in cluster minikube
💾  Downloading Kubernetes v1.27.4 preload ...
    > preloaded-images-k8s-v18-v1...:  393.21 MiB / 393.21 MiB  100.00% 7.38 Mi
🔥  Creating virtualbox VM (CPUs=2, Memory=3900MB, Disk=20000MB) ...
🐳  Preparing Kubernetes v1.27.4 on Docker 24.0.4 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

Check if we are connected to kubernetes:
```bash
~➤ cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /home/n0kt/.minikube/ca.crt
    extensions:
    - extension:
        last-update: Thu, 05 Oct 2023 17:54:08 -04
        provider: minikube.sigs.k8s.io
        version: v1.31.2
      name: cluster_info
    server: https://192.168.59.115:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    extensions:
    - extension:
        last-update: Thu, 05 Oct 2023 17:54:08 -04
        provider: minikube.sigs.k8s.io
        version: v1.31.2
      name: context_info
    namespace: default
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /home/n0kt/.minikube/profiles/minikube/client.crt
    client-key: /home/n0kt/.minikube/profiles/minikube/client.key

```

```bash
~z➤ kubectl get pods --all-namespaces
NAMESPACE     NAME                               READY   STATUS    RESTARTS      AGE
kube-system   coredns-5d78c9869d-65s49           1/1     Running   0             47s
kube-system   etcd-minikube                      1/1     Running   0             60s
kube-system   kube-apiserver-minikube            1/1     Running   0             59s
kube-system   kube-controller-manager-minikube   1/1     Running   0             59s
kube-system   kube-proxy-zgpqq                   1/1     Running   0             47s
kube-system   kube-scheduler-minikube            1/1     Running   0             59s
kube-system   storage-provisioner                1/1     Running   1 (46s ago)   58s

```

Stop and Delete the cluster:
```bash
minikube stop
minikube delete
```
