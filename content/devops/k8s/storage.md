# Storage

## Volumes
Containers state are ephemeral, once the container is terminated then the Controller will recreate the container but data from the crashed/deleted container is lost. We can persist the container or containers data by using **Volumes**, but it will last only while the Pod is alive, once the Pod is eliminated then the volume is gone.

- More references: `kubectl explain pod.spec.volumes`
- Pod have shared filesystem so all containers can share the files with a `volume`
- Ephemeral Volumes: emptyDir, configMap, secrets
- Persistent Volumes: hostPath, local, ebs (aws), etc

**Mount propagation**: Which can be `None`, `HostToContainer`, `Bidirectional`. This is about mounts on top of mounted volumes.

## Persistent Volumes
These volumes can persist even if the Pod is terminated.
- `PersistentVolume`: Piece of Storage attached to the cluster by an Administrator
- `PersistentVolumeClaim`: Request to a storage space by an user (Pods)

**How PV and PVC work together**: PV controller monitor Etcd looking for PVCs if found the it searchs for a valid PV and bound to it If not then checks for the storage class for dynamic provisioning of PV. Each storageClass have its own Provisioner.

Notes:
- If a PVC is deleted then it waits until no Pod is using it. If a PV is deleted then it waits until no PVC is using it.
- A PV binding to a PVC is 1 to 1 mapping only.
- volumeMode:
    - `Filesystem`: if the volume backed by a device is empty, k8s creates a filesystem before mounting it
    - `Block`: No filesystem layer, much faster to write, the app in the pod needs to know how to handle Raw Block device
- acccessMode: ReadWriteOnce, ReadOnlyMany, ReadWriteMany, ReadWriteOncePod
- storageClassName: if this is defined then the PVCs can get a PV with the specific class name
- persistentVolumeReclaimPolicy:
    - Retain: PVC is deleted but not the PV and also the storage
    - Delete: PVC and PV are deleted as well as the storage
    - Recycle: Performs rm -rf in the volume and it's available for new claims
- One single PVC can be used by multiple containers and use different folders by using: `subPath` and `subPathExpr`
- When using type "local", k8s will make sure Pods that uses that PV are allocated in the nodeAffinity of the PV.
    - The PV and local type must have nodeAffinity defined.

## Persistent Volume Claim 
These PVC have some properties similar from PVs and also:
- Selectors: The matchLabels and matchExpressions is ANDed and help to bound a PVC witht the PV.
- Class: the class name PV where the PVC will be bound, of not specified then will be bound to the kids default classStorage, it can also be empty string "".

### Snapshots
- A PVC can be created from a volume snapshots via `.spec.dataSource`. It can also be created from another existing PVC.
- PVC can also be prepopulated via `.spec.dataSourceRef` and a Custom Resource.

## Storage Class
- Kubernetes has a default storageClass, it can have multilples but the latest one will have priority.
- Each storageClass have its own Providioner that creates PVs

## Volume Snapshots
- VolumeSnapshotContent is the resource and VolumeSnapshot is the request to create snapshots.
- These snapshots can be pre-provsioned (manual creation of VolumeSnapshotContent) or Dynamic (via VolumeSnapshot) from a PVC
## Notes for the lab
no
- 00: Pod with Volume `emptyDir`
- 01: Pod NFS Volume
- 02: Configmap & secrets, read only
- 03: PV and PVC with `local` and `hostPath`
- 04: Storage Class with EBS
    - Reclaiming: Delete, Retain and Recycle
- 05: Volume Snapshots
Meh
