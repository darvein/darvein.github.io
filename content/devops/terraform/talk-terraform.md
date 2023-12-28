# Terraform talk (30min)

## Topics to cover: 
- what is for terraform
- How it works 
- TF main parts (provider, resources, variables, outputs, backend, templates/data, provisioners, null_resource, data+program+bash, ) 
- Where not to use it / when to use it
- Syntax and programming + tricks (variables types,maps,locals, tulle, objects) 
- Logic: loops, conditionals, 
- TF env vars for vars 
- Modules usage and creation 
- Terraform registry
- Workspaces
- Remote states 
- Secrets
- Locking state (s3, dynamodb)
- Integrations: Vault, ansible, chef, packer, user data , aws secrets, 
- Terraform and docker (ECS/EKS)
- Terraform and machine learning? 
- Grunt work framework
- TF testing: terratest, curl, kitchen-terraform, rspec-Terraform 
- Documentation and generators 
- Terraform plug-ins?
- Best practices
- 

## TF limitations
- cannot use loops/foreachs while calling modules

## Things to review:
- terraform graph 
- Demo with JQ
- production-grade infra checklist
- cloud nuke - Aws-nuke 
- Chaos monkey / janitor monkey 
- golang “dep ensure”

## TF modules
- have to be small, composable, testable




## Talk agenda for 30min

- What is IaaC?
    - what is terraform
    - what problem does it solves?
    - when and when not to use IaaC
- How terraform works?
    - basic workflow of work
    - terraform underneath and API calls to AWS
    - workspaces
    - TF registry
- Terraform code and syntax
    - about HCL
    - variable types: maps, locals, tuples, objects
    - things to use: provider, resources, variables, outputs, backend, null_resource
    - logic: loops, conditionals
    - built-in functions of TF
    - data, templates, data+program+bash
    - secrets storage
    - directory layout
- Modules
    - how to create them
    - how to use them
    - module best practices
- Collaborative work 
    - TF remote state in TF cloud ui
    - TF locking and s3+dynamodb
- Code testing
    - terratest, curl, kitchen-terrafor, rspec-terraform
- Documentation
    - doc generator
    - graphs generator
- TF and the ecosystem
    - Ansible, chef, packef, user data, aws secrets
    - docker, ECS/EKS
    - machine learning
- Resources to keep learning
    - https://www.terraform-best-practices.com
    - https://www.terraform.io/docs/configuration/index.html
    - https://www.terraform.io/docs/cloud/guides/recommended-practices/part1.html
