+++
title = "Ser Devops estresa un poco"
categories = ["Devops", ]
date = "2023-05-22"
+++

La otra vez estaba en mi escritorio haciendo mis tickets jira y revisando algunos reportes de google, cuando de repente mensaje salvaje aparece en mi escritorio, si, no miento, era un mensaje donde decía que Producción esta inestable. Estoy en un nuevo proyecto y aún me estoy familiarizando con las aplicaciones, bueno pero con las pistas que me dieron era obvio que algo andaba mal con el servicio de Kafka.

Me tarde un rato en darme cuenta que el servicio Kafka no lo tenían corriendo en Kubernetes sino el de AWS MSK. Entonces primeramente fuí a ver que los nodos esten respondiendo.

```bash
# Getting bootstrap brokers
~» aws kafka get-bootstrap-brokers \
        --cluster-arn ********
{
    "BootstrapBrokerString": "********",
    "BootstrapBrokerStringTls": "********",
    "BootstrapBrokerStringSaslScram": "********"
}
```

Cada de ellos respondía bién sin novedades.
```bash
~» kafka-topics.sh --list --bootstrap-server ********
LIncidentStrDevV4r
LIncidentStrStagingV4r
LIncidentStrV4R3r
LIncidentStrV6r
LSourceOStrV4r
LSourceOStrV4R2r
LSourceOStrWithLatchingDevV4r
LSourceOStrWithLatchingStagingV4r
LSourceOStrWithLatchingV4r
LSourceOStrWithLatchingV6r
LTargetOStrV4r
LTargetOStrV4R2r
LTargetOStrWithLatchingDevV4r
LTargetOStrWithLatchingStagingV4r
LTargetOStrWithLatchingV4r
LTargetOStrWithLatchingV6r
LVideoStrDevV4r
LVideoStrStagingV4-calc
LVideoStrStagingV4r
LVideoStrV4-calc
LVideoStrV4r
__amazon_msk_canary
__amazon_msk_canary_state
__consumer_offsets
```

Todo parecía normal, revisé logs, revisé métricas, etc. No encontraba nada y Producción al parecer ya estaba bién (misterio total). Revisando cosas por AWS Dashboard justo se me ocurrió leer una de las notificaciones, de esas que te aparecen en la esquina superior derecha y ví esto:

{{< limg "/i/2023-05-22_19-36.png" "Los mantenimientos de AWS" >}} 

Era un mantenimiento de seguridad de AWS, según ellos el cluster debería estar operacional para las aplicaciones, si es que se estan siguiendo algunas buenas prácticas de clusterización. Al menos me puse a revisar el RF en algunos Topics (aquellos directamente relacionados con las apps que reportaron inestables), para asegurar de que al menos sean 3.

```bash
~» kafka-topics.sh \
        --describe \
        --bootstrap-server ********:9092 \
        --topic MehMehMehKey
Topic: MehMehRaw        TopicId: **** PartitionCount: 10     ReplicationFactor: 3    
Configs: min.insync.replicas=2,message.format.version=3.0-IV1,...

    Topic: MehMehMehKey        Partition: 0    Leader: 3       Replicas: 3,1,2 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 1    Leader: 2       Replicas: 2,3,1 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 2    Leader: 1       Replicas: 1,2,3 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 3    Leader: 3       Replicas: 3,2,1 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 4    Leader: 2       Replicas: 2,1,3 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 5    Leader: 1       Replicas: 1,3,2 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 6    Leader: 3       Replicas: 3,1,2 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 7    Leader: 2       Replicas: 2,3,1 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 8    Leader: 1       Replicas: 1,2,3 Isr: 2,1,3
    Topic: MehMehRaw        Partition: 9    Leader: 3       Replicas: 3,2,1 Isr: 2,1,3
```

Dado que ya no se reportaban mas problemas en Producción, tomando en cuanta que hubo un mantenimiento de AWS y que nadié recibió apropiadamente el email y además que de un momento a otro ya nadié se quejó mas por la inestabilidad... sólo queda decir que estas personas solo me hacen estresar sin motivo, yo tan feliz que estaba en mi escritorio, mas bién nada grave, pero al menos me estresé por una hora.

Santo remedio, salir a caminar

{{< limg "/i/20230517_095626.jpg" "Viéndome yo mismo como el muchacho de El Alquimista" >}} 
