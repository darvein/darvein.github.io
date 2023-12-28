# Workloads

This is a brief of documentation from https://kubernetes.io/docs/concepts/

# Content

- [Kubernetes Notes](#kubernetes-notes)
- [Content](#content)
    - [Concepts](#concepts)
        - [Objects in kubernetes](#objects-in-kubernetes)
        - [Kubernetes components](#kubernetes-components)
        - [On-prem scenarios](#on-prem-scenarios)
        - [Containers](#containers)
        - [Workloads](#workloads)
            - [Pods](#pods)
            - [Workload resources](#workload-resources)
                - [Deployments](#deployments)
                - [ReplicaSet](#replicaset)
                - [StatefulSet](#statefulset)
                - [DaemonSet](#daemonset)
                - [Jobs](#jobs)
                - [Cronjob](#cronjob)
                - [ReplicationController](#replicationcontroller)
    - [Topics to review](#topics-to-review)
    - [Random notes](#random-notes)
    - [TODOs](#todos)

## Concepts
Kubernetes solves problem of resource allocation

### Objects in kubernetes
- Pods have unique name
- All k8s objects have an UID
- `labels` and `selectors` to tag and organize objects, helpful from cli or UI. 
    - `kubectl get pods -l environment=production,tier=frontend`
    - `kubectl get pods -l 'environment,environment notin (frontend)'`
    - Recommended labels:
    ```yaml
    app.kubernetes.io/name: mysql
    app.kubernetes.io/instance: mysql-abcxzy
    app.kubernetes.io/version: "5.7.21"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: wordpress
    app.kubernetes.io/managed-by: helm
    ```
- Namespaces, are used as environments (useful to allocate users via Resource Quota)
    - DNS when creating a service: `<service-name>.<namespace-name>.svc.cluster.local`
    - Not everything has a namespace, see what are those: `kubectl api-resources --namespaced=false`
- Annotations, not queri-able like Labels and can contain structured & unstructured obj information (build, client lib info, urls, etc)
- Owners and dependents, for eg. **ReplicaSet** is owner of a set of **Pods**, **Service** owns **EndpointSlice**.

### Kubernetes components
**Control Plane**:
- kube-apiserver: exposes k8s API, scales horizontally (scales by deploying more insatnces of the app)
- etcd: HA key-value store for cluster data
- kube-scheduler: watches new pods without nodes, selects a node for them to run. Manages scheduling decisions(hardware/software/policy constraints, affinity, etc)
- kube-controler-manager: multiple controllers into a single binary (node, job, endpointslice, serviceAccount controllers)
- cloud-controller-manager: bunch of binaries (node, route, service controllers)

**Node components**:
- kubelet: make sure containers are running in a pod
- kube-proxy: network proxy that allow pods communicate inside/outside of the cluster

### On-prem scenarios
- Ansible Kubespray (for medium-large setups)
- Kubeadm (for small, demos)
- Rancher RKE `rke up` (it requieres cluster.yml)
- Redhat Openshift
- VMware Tanzu Kubernetes

Reasons?: Compliances, cheaper, agnostic, 

Critical components:
- Etcd HA (backups)
- LB: f5, metallb, haproxy
- HA: multiple nodes AZ
- Persistent Storage: via CSI plugins (block or file storage)
- Upgrades, every 3 mo
- Master nodes, quorum min 3, max 7
- Node reqs: 32 cpu cores, 2tb ram?, 4 SSDs, 8 Sata SSDs, 2 10G eths

### Containers
A container image is like a software package that is inmutable. A container engine is the service where the image is executed/ran. Kubernetes supports container runtimes accepted by CRI (container runtime interface) like docker, containerd, cri-o.

Kubernetes has `imagePullPolicy` pull policy that specifies whether k8s should pull always `Always`, never `Never` or if the image doesn't exist locally `IfNotPresent`. As best practice, avoid using `:latest` images, it makes harder to rollback to previous image which is also `:latest`. You can also specify an image digest in the name: `server-image.com:image-name:thetag@sha256:xxxxxxxxxxxxx`

**Authentication**, keep in mind that Kubernetes needs to be authenticated against the Image Repository by using k8s Secrets.

### Workloads
Container images are deployed in Pods on kubernetes. Kubernetes itself manages the workload via Controllers to make sure Pods are properly created across the cluster nodes

The following are built-in workload objects: Deployment and ReplicaSet, StatefulSet, DaemonSet, Job and CronJob. If you need to have an special kind of workload that doesn't exist you can create your own by using a CRD (custom resource definition).

#### Pods
- Pods are created on your behalf via _Deployment_, _StatefulSet_ or _DaemonSet_
- Pods can share context via linux namespaces, cgroups. So multiple containers can run in the same context.
    - Containers in the pod share the same networ, same IP
    - Containers can share Storage volume
    - A container in a pod can run with enabled privileges via `privileged` on linux, on windows is `windowsOptions.hostProcess`
- A pod can have a single container or multiple containers (logs/metrics collection, config reload watcher, proxies like envoy/istio)
- You can modify a running Pod via `patch` or `replace` but it has limitations. You cannot modify most of the metadata. Maybe `spec.containers[*]`, `spec.initContainers[*]`, `spec.tolerations`
- Lifecycle: `Pending`, `Running`, `Succeeded`, `Failed`, `Unknown`
- Probes:
    - Check mechanisms: `exec`, `grpc`, `httpGet`, `tcpSocket`
    - Probe outcome: `Success`, `Failure`, `Unknown`
    - Types of probe: `livenessProbe`, `readinessProbe`, `startupProbe`
- Termination of a pod: By default it has a grace of 30 seconds via signal `SIGTERM`. Or rather you can specify `--grace-period=0` to quickly terminate the pod.
- Pod can have Init Containers, these are containers that are first executed in order to do some previous work before running the App Containers. Work like cloning a git repo, configuring or resolving secrets, just waiting for some external http dependencies, etc.
    - There can be multiple init containers defined in `spec` in the manifest yaml file
    - Init containers cannot have ports linked to a Service
    - A pod cannot be `Ready` until init containers have succeeded
- PodDisruptionBudget (?)
- You cannot add containers to a running Pod
    - You need to troubleshoot? then *Ephemeral Containers* via `kubectl debug (POD_NAME) --image=(DEBUG_IMAGE) --target=(EXISTING_CONTAINER_NAME)`. Once this is running then you can `kubectl attach` or `kubectl exec`, then start analyzing the Pod.

#### Workload resources
Built-in workloads are:
- Deployment (ReplicaSet indirectly)
- StatefulSet
- Daemonset
- Job & Cronjob

##### Deployments
Deployment -> ReplicaSet -> Pod. This is managed by the Deployment Controller in k8s master cluster.

We can do:
- Check deployment status: `k get deployments`
- Rollout status: `k rollout status deployment/nginx-deployment`
- Rollout history: `k rollout history deployment/nginx-deployment`
- Rollout rollback via undo: `k rollout undo deployment/nginx-deployment`
- Scaling a Deployment: `k scale deployment/nginx-deployment --replicas=10`
- Check the replica sets: `k get rs`
- Update a Deployment: `k set image deployment/nginx-deployment nginx=nginx:1.16.1`
- Edit a Deployment: `k edit deployment/nginx-deployment`
- Describe a Deployment: `k describe deployment/nginx-deployment`
    - It is important to pay attention to the **Conditions:** section, there you can see errors if any
- Via deployment spec `.spec.strategy` we can specify **RollingUpdate** or **Recreate** deployments. Also the proportional rolling deployments

##### ReplicaSet
- Get RS: `k get rs`
- Describe RS: `kubectl describe rs/frontend`
- Delete a RS: Can be done via `k delete` but also via `k proxy` k8s API. We can delete the RS and its Pods or just the RS alone.
- A RS can be scaled via HPA (horizontal pod autoscaler) **HorizontalPodAutoscaler** kind object where we specify a RS, minReplicas, maxReplicas, it can also work via cli `k autoscale rs frontend --max=10 --min=3 --cpu-percent=50`

##### StatefulSet
- Works similar to **Deployment** but not controls via RS Controller it uses StatefulSet Controller instead
- Statefulset unline Deployment is not interchangeable, a pod can die and a new one born with different IP or name, a Statefulste pod if dies will always be recreated with same name and IP and its replicas will be numered like `web-0`, `web-1`, etc.
- It has stable and persistent Storage
- This StatefulSet have: unique network identifiers, persistent storage, ordered and graceful deployments/scalings/rolling
    - Storave PVC is only for one uniq statefulset pod, it is not shared with other pods
- Deployments: Termination of pods are in reverse order. Before Scaling all pods predecessors must be Running/Ready
    - Pods are Started, Scaled, Terminated in a strict order FIFO
    - No rollbacks allowed
    - Via `.spec.updateStrategy.type` property can be specified **RollingUpdate** and Partitions(?)
        - It can also specify `.spec.updateStrategy.rollingUpdate.maxUnavailable`
- Storage have policies via `spec.persistentVolumeClaimRetentionPolicy`
    - Volumes are not deleted by default (when deleting the pod or scaling down)
    - By default it **Retain** a PVC, but it can also be **Delete**, when **whenDeleted** or **whenScaled**
    ```yaml
    spec:
      persistentVolumeClaimRetentionPolicy:
        whenDeleted: Retain
        whenScaled: Delete
    ```
- It requires **Headless Services** for network identity, this way it doesn't load-balance anything as it is not needed.
- When a PVC/PV is created for a Statefulset service, if not specified by default will use the `hostPath` storage type.

##### DaemonSet
Pods defined as **DaemonSet** are ensured to run across all nodes, one copy each node via DaemonSet Controller.

Use cases: cluster storage daemon, logs collection, node monitoring

Notes:
- Via `spec.affinity.nodeAffinity` 
    ```yaml
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchFields:
          - key: metadata.name
            operator: In
            values:
            - target-host-name
    ```
- Communication:
    - Service: a service can be put on top (via labels matching) and then reach a random pod daemon from any node
    - DNS: via `endpoints` discover daemonsets via pod selectors

##### Jobs
Runs a pod until it succesfully terminates (exit code 0). If the pod fails for some reason then it is run again.

Notes:
- The `RestartPolicy` can be *Never* or *OnFailure* only
- Parallelism
    - Jobs can be run on parallel or not based on properties `.spec.completions` and `.spec.parallelism`
        - If not specified, both values are defaulted to 1
    - `completionMode` can be **Indexed** or **NonIndexed**. 
        - When **Indexed**: at least one of the jobs in the index cluster has to be success in order to complete the job
        - When **NonIndexed**: all jobs have to be completed succesfully in order to consider the job completed
- Failures
    - Can be specified in `.spec.backoffLimit`, by default is `6` with exponential back-off delays (10s, 20s, 40s)
    - Each index job can also have its back off limit via `.spec.backoffLimitPerIndex`
    - `restartPolicy` has to be set to **Never**
    - Example:
        ```yaml
        apiVersion: batch/v1
        kind: Job
        metadata:
          name: job-backoff-limit-per-index-example
        spec:
          completions: 10
          parallelism: 3
          completionMode: Indexed  # required for the feature
          backoffLimitPerIndex: 1  # maximal number of failures per index
          maxFailedIndexes: 5      # maximal number of failed indexes before terminating the Job execution
          template:
            spec:
              restartPolicy: Never # required for the feature.
              containers:
              - name: example
                image: python
                command:
                      - id
        ```
    - Pod failure policy: we can customize and exit codes:
        ```yaml
        ...
        backoffLimit: 6             # This retries the whole job, it also works for parallelism
      podFailurePolicy:
        rules:
        - action: FailJob
          onExitCodes:
            containerName: main      # optional
            operator: In             # one of: In, NotIn
            values: [42]
        - action: Ignore             # one of: Ignore, FailJob, Count
          onPodConditions:
          - type: DisruptionTarget   # indicates Pod disruption
        ```
        - Valid Actions are: FailJob, Ignore, Count, FailIndex
- Clean up and Terminations:
    - By default the Job and Pods are not removed, in case you want to check logs. You have to manually delete via `k delete`
    - We can kill longer job pods via `.spec.activeDeadlineSeconds` property if we want to limit time execution
    - We can automatically clean up jobs and pods if we want via prop `.spec.ttlSecondsAfterFinished`
- Jobs pods can be suspended (suspended=true)

Then we can check the status with: `k get -o yaml job job-backoff-limit-per-index-example`

##### Cronjob
Cronjob creates Jobs on  a repeating schedule.

Some definitions:
- You can specify timezone: `spec.timeZone: "Etc/UTC"`

Use cases: backups, report generation

Notes:
- It specifies a `.spec.jobTemplate` section
    - Via `.spec.schedule` we define when to run the job
- It supports concurrency via `.spec.concurrencyPolicy` with values: Allow, Forbid, Replace

##### ReplicationController
Ensure the specified number of pods are running in the cluster. It is similar to a Deployment. Deployment is replacement of ReplicationController.

## Topics to review
- Kubernetes architecture: control plane, etcd, api server, scheduler, controllers
    - nodes: kubelet, container runtime, kube-proxy
    - authentication and authorization
- How docker works?
- deployment & services
- configuration & secrets
- ingress, statefulset, daemonset, jobs, crds
- network policies, persisten volumes, storage classes
- prometheus, grafana elk, fluentd
- helm, fluxcd
- rbac, security contexts
- scaling: HPA and VPA, cluster autoscaling

## Random notes
- kubectl exec, happens thanks to kube-api, kubelete and websockets via HTTPS
- each pod has cgroups to limit resource allocations

## TODOs
- Learn linux namespaces & cgroups
- PoC run two containers in a pod. Ping container A to container B.
