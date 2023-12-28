# Introducción a Kubernetes

## ¿Qué es Kubernetes?

- Es un orquestrador de contenedores
- Opensource toolkit desarrollado por Google (2014)
- También deminado K8S
- El diseño de K8S está basado en 4 principios:
  - Escalabilidad
  - Disponibilidad
  - Seguridad
  - Portabilidad

---

### Contenedores para aplicaciones (Docker)

- Docker es una plataforma con el que se puede ejecutar una aplicación de forma aislada en un sistema operativo
- El empaquetamiento de imágenes docker y la ejecución de las mismas en contenedores permiten crear ambientes de desarrollo y producción consistentes

### Microservicios

- Fácil mantenimiento a largo plazo
- Facilidad al momento de agregar, actualizar o quitar alguna tecnología de software
- Facilidad de escalamiento horizontal de la aplicación

---

## ¿Para que sirve Kubernetes?

- Para orquestrar contendedores
- Facilita la operatibilidad de empaquetar, integrar, testear, y desplegar aplicaciones en servidores
- Provision de estrategias y mecanismos confiables y seguros de despliegue de software
- Facilita el mantenimiento y desarrollo de plataformas tolerantes a fallo, escalables y de alta disponibilidad

---

## Características de K8S

- Es instalable en cualquier tipo de infrastructura:
 * Cloud (Google Cloud **GKE**, AWS **EKS**, Azure **EKS**, etc)
 * Infrastructura local o privada
 * Híbrido de infrastructuras públicas y privadas
- Funcionalidad especifica o avanzada puede ser desarrollada atravéz de **Operators** (operadores)
- Provisión de diferentes capacidades y funcionalidades
  - Montaje de diferentes sistemas de almacenamiento
  - Manejo y distribución de datos sensitivos (secrets)
  - Verificación automática de la salud de las apps en contendedores
  - Balanceo de carga
  - Actualizaciones continuas (zero-downtime)
  - Manejo de autenticación y autorización

---

## Alternativas a Kubernetes

- Mesosphere
- Docker Swarm
- Docker Compose (desarollo local)
- Docker Cloud
- Minikube (desarollo local)

---

# Architectura de Kubernetes

Kubernetes está básicamente compuesto por:

- Master: El nodo o servidor primario del cluster
- Worker node: Que vendría a ser un worker o slave del cluster

## Principios de operación

- Todos los contenedores son encapsulados y orquestrados en **Pods**
- Los recursos necesarios para levantar un contenedor son dinámicamente asignados y reservados en los diferentes nodos disponibles por Kubernetes
- Todos los mensajes de las aplicaciones son centralizadas en un solo lugar
- Todas las métricas de los recursos del cluster son centralizadas en un solo lugar

--- 

## Componentes internos

- API Server
- Scheduler
- Datastore (ETCD)
- Controler manager

## Componentes externos

- Docker
- Kubelet
- kube-proxy
- kubectl

## Componentes adicionales

- Monitoring
- Logging
- Service discovery

--- 

# Autenticación y autorización en Kubernetes

## Proceso de Autenticación

- Regular users
- Service accounts

#### Diferentes métodos de autenticación

- Certificados de cliente x509
- Bearer tokens
- Usuario y contraseña

## Proceso de Autorización

- AlwaysDeny
- AlwaysAllow
- RBAC (Role based access control)
- Node
- Webhook

---

# Referencias

#### Sitios web
* [Kubernetes architecture](https://kubernetes.io/docs/concepts/architecture/)
* [Kubernetes overview](https://thenewstack.io/kubernetes-an-overview/)
* [Kubernetes architecture 101](https://www.aquasec.com/wiki/display/containers/Kubernetes+Architecture+101)

#### Libros
* Mastering Kubernetes (Second edition) - Gigi Sayfan
