# Kubernetes security

In a nutshell these are the most important aspects to consider:
1. Cloud security
2. Cluster security
3. Network security
4. Container security
5. Secrets Management

## Cloud security
The documentation mention the 4Cs:
- Cloud: best practices
- Cluster: control plane protection, encryption, security policies
- Container: image scanners, pod security
- Code: dynamic attack testing, static analyzis

In case of AWS what security involves:
- IAM: users, groups, roles, policies
- Networking: VPC security-groups, NACLs, AWS Shield
- Data encryption: KMS, in-transit (tls/ssl, vpn)
- Monitoring and Logging: Cloudwatch , Cloudtrail
- Etc: Guarduty, AWS Config, SCPs

## Cluster Security
### Node security
Some Node security best practices
- Regularey patch and update the OS
- Secure components like kubelet, kube-proxy, and container runtime
    - Always authentication enabled, PSPs, Network Policies
    - Limit Memory and CPU
- Audit Logs and have Intrusion detection software

### Control plane security
Most important components to keep in mind:
- API Server: 
    - Authentication: X.509, Tokens (static file, bootstrap, service account), OIDC (oauth 2.0), Webhook/Proxy.
    - Authorization: RBAC, ABAC, Webhook Proxy
    - Admission Control: Modifies or Rejects incoming requests. Enforces additional policies.
- ETCD
    - Authentication and Authorization & Encryption at rest
    - Disaster recovery plan: Snapshots, Test backups.

## Container Security
### Pod Security Policies (Deprecated from k8s v1.21)
Pods have 3 security policies profiles: Privileged, Baseline and Restricted.
It manages features like:
- Privileges: non-root, RunAsUser, RunAsGroup
- Volume types
- Host namespaces: ipc, pid, host network
- SELinux
- FSGroup
- Allowed Capabilities
- Seccomp

### Pod Security Standrads Admission controller
The namespace has to be labeled with the desired level such as: `privileged`, `baseline`, `restricted`.

It also supports modes, where the Admission Controller can still permit or not even if the level has been rejected, these modes are: `audit`, `warn`, `enforce`.

Admission controller for this also supports **Exemptions** where we can bypass or allow certain namespaces, users or runtime classes. This works at cluster level via `kind: AdmissionConfiguration`

These profiles are based on the deprecated Pod Security Policies.

#### Privileged
This is unrestricted.

#### Baseline
The following are the limitations, what a Pod won't be able to do:
- Run as privileged: access to host devices, execute privileged operations
- Use host namespaces: Not allowed to share host's network, IPC or PID
- Mount HosPath Volumes
- Bind Host Ports
- Run as Root, unless you set `allowePrivilegeEscalation` to `false`
- Cannot add additional Capabilities other than the assigned by the container runtime
- Custom Seccomp profiles, onlye the default from the runtime. Same with SELinux

#### Restricted
- All from Baseline
- Disallow Privilege Escalation
- Immutable root filesystem
- Disallow more dangerous capabilities

### Container security
Best practices:
- Use well-known images: alpine, debian:slim, ubuntu:latest
- Minimize `RUN` commands, minimize them into one
- Avoid using `root` user
- Scan the container image: Claire, Tenable, Aqua Trivy

## TODOs
- Security pods and hosts: seccomp, apparmor, selinux
- Multi-tenancy

## Labs
1. Pod security standards (privileged, baseline, restricted)
2. Role creation, Service Account
3. Service Accounts and Tokens
4. AWS OIDC and kubernetes
