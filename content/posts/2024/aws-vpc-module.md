---
title: "AWS VPC Module"
categories: ["Mente"]
tags: ["Tecnología"]
date: "2024-06-25"
thumbnail: "/i/aws-vpc-mod.jpg"
draft: true
---

### El primer paso
Bueno, estoy motivado a escribir web apps, pero no puedo hacer mucho si no tengo lista la infraestructura en la nube. Talvez estoy exagerando pero en su momento voy a necesitar levantar servicios en la nube para poder desplegar mis aplicaciones (Ajá..., tengo planeado hacer miles de apps 😅).

He notado que ya existen varios proyectos en Github y por ende en **Terraform Registry** proyectos que ya levantan VPCs en AWS, pero hoy tengo ganas de tener el mio que sea mas cool. Quiero que sea amigable para el tema de creación de SGs y NACLs externos, quiero que maneje cosas como Cloudwatch, VPC Peering y Sharing, VPC Endpoints, TGW, etc. Quiero tener un módulo con el que pueda manejar la mayor parte posible del tema de Red en AWS. Entonces en lugar de usar este repo [terraform-aws-vpc](https://github.com/terraform-aws-modules/terraform-aws-vpc) estoy creando el mio propio. 

**Proyecto => [tf-aws-vpc](https://github.com/darvein/tf-aws-vpc)** :see_no_evil:

Además que estoy motivado a seguir repasando y mejorando mis habilidades en esta tecnología en la nube de AWS (Amazon Web Services) y nada mejor que ir de la mano de Terraform para automatizar mis scripts para poder levantar todo lo necesario en cuestión de VPCs para mis proyectos.

Por ahora logré avanzar el modulo y crear las subnets, este sería mi *HolaMundo* en este proyecto, me agrada como lo estoy armando. Además se podrán dar cuenta que tuve que crear otro módulo para el etiquetado de los recursos, algo asi como lo hace **CloudPosse**, nada mas que yo estoy siguiendo algunas buenas prácticas de la industria para el etiquetado de los mismos recursos en AWS.


```terraform
module "tags" {
  source = "github.com/darvein/tf-tags?ref=v0.1"

  tags = {
    Environment = "Development"
    Customer = "ACME"
    Team     = "Nextbrave"
  }
}

module "vpc" {
  source     = "../"
  cidr_block = var.cidr_block

  public_subnets   = local.public_subnets
  private_subnets  = local.private_subnets
  internal_subnets = local.internal_subnets

  tags = merge(module.tags.all, {
    Tier = "Network"
  })
}
```

### NAT e Internet Gateways

...

![foobar](../../i/20240610_074059.jpg)


```text
┏━━━━━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━━━━┓
❍  Carpe Diem ・┈┈・ Memento Mori.  ❍
┗━━━━━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━━━━┛

              _.-/`)
             // / / )
          .=// / / / )
         //`/ / / / /
        // /     ` /
        ||         /
        \\       /
         ))    .'
        //    /
             /
```
