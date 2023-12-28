# Devops Interviews

I'm writing down for the first time the pattern I've found across all my interviews :+1:

Currently this document is a Draft, I will keep updating this while I remember all my interview cases.

## Your introduction
Here you already have to have a prepared introduction, you will not be interrumped, so you will have to memorize it.

Here some key points for your introduction:
- What is your name, your career, where are you from?
- How many years you are working so far?
- What certifications you archived?
- What types of industries you worked for? (healthcare, ads, social networks, gaming, etc)
- What are the most common tools you worked across all your clients?
- What do you do nowadays? (related to technology)

## Preparation
- Be on time, be at least 10 minutes online and test your equipment
- Make sure you have a working microphone and camera
- Grab a pen & paper to take notes of things you need to improve
- If you need to reschedule, do it at least 1-2 hours before the meeting

## Screening/Introduction calls
**Purpose of the call**: Get to know each other, Company and Candidate.

The flow is as follows:
1. Who we are (the company side)
2. Who I am (candidate side). Just brief introduction
3. Test your english level (in case the interview is not in english)
   - How is your daily work?
   - How is your city?
   - How you are up-to-date with internet news?
4. What is your rate?

**Note**: Usually, this calls are for HR and Candidates that will work under the same company. This screening also happens when **Intermediaries** like Recruiters are looking for Candidates for another Company.

**Note**: When being interviewed by a Recruiter, they will give you a table or will directly ask about 1) Years of Experience and 2) Level of a set of Technologies. Just answer like this:
- Years of experience and Level on: Kubernetes. Say 10000 Years, God Level
- Years of experience and Level on: Docker. Say 10000 Years, God Level
- Years of experience and Level on: Jenkins. Say 10000 Years, God Level
- Years of experience and Level on: CI/CD Pipelines. Say 10000 Years, God Level
- Years of experience and Level on: AWS. Say 10000 Years, God Level
- Years of experience and Level on: Terraform. Say 10000 Years, God Level
- Years of experience and Level on: Bash Scripting. Say 10000 Years, God Level
- So on and so on...

## Technical interview - Simple
**Purpose of the call**: Test your skills without going depth. Usually a Manager, Team Lead, or any other person with avergage knowledge :see_no_evil:

Domain: Linux
| Question                           | Expectation                                                                                                                      |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Linux commands, what are they for? | You have to explain how they work underneath and what is the purpose of some of them: `ps`, `netstat/ss`, `fdisk`, `free`, `top` |

Domain: AWS
| Question                                               | Expectation                                                                              |
|--------------------------------------------------------|------------------------------------------------------------------------------------------|
| What services you worked in AWS                        | To be familiarized with basic services in Compute, Storage, Databases and Networking     |
| Explain differences of a Public vs Private AWS Subnets | You have to explain the VPC Components to make a subnet public/private and how they work |

Domain: CI/CD
| Question                                        | Expectation                                                                                    |
|-------------------------------------------------|------------------------------------------------------------------------------------------------|
| Explain what CI/CD is                           | Describe CI and CD and the most common stages                                                  |
| What CI/CD tools you worked?                    | Just mention the most common ones like Github Actions, JEnkins, Bitbucket Pipelines, Gitlab CI |
| Difference of Continous Deployment and Delivery | Explain what is each of them while providing use cases                                         |

Domain: Containers
| Question                                         | Expectation                                                                     |
|--------------------------------------------------|---------------------------------------------------------------------------------|
| What is docker, how it works?                    | Explain Docker components and how they interact                                 |
| Alternatives to docker?                          | Mention the alternatives and how they are different from docker                 |
| Difference of Kubernetes Deployment vs Daemonset | Mention the use cases for each Deployment, Statefulset, DaemonSet, Job, Cronjob |


Domain: IaaC
| Question                            | Expectation                                                          |
|-------------------------------------|----------------------------------------------------------------------|
| How Terraform works?                | Explain how TF communicates with Providers, how it manages the state |
| What are some commands of terraform | Explain the regular workflow of commands                             |

Domain: Experience
| Question                                   | Expectation                                                                                            |
|--------------------------------------------|--------------------------------------------------------------------------------------------------------|
| How you manage an slowness issue?          | Explain how you go from top to bottom (networking, app server, databaser, caching servers, app, APM, ) |
| What you did on your last project/company? | Mention the most relevant outcomes, how you gave value to the company                                  |

## Technical interview - Comprenhensive or Client side
Domain: AWS
| Question                              | Expectation                                           |
|---------------------------------------|-------------------------------------------------------|
| What features offers RDS Aurora       | Mention HA, DR use case, Pricing                      |
| How AWS ASG works?                    | Explain manual scaling, Scaling with Cloudwatch       |
| How to connect 2 VPCs or More?        | Explain about VPC Peering and Transit Gateways        |
| How to access an EC2 without key      | Explain about EBS & Snapshots, Recreation of EC2      |
| Difference of AWS LB Classic vs ALB   | Explain TCP vs TCP HTTP (http headers and properties) |
| AWS Global Accelerator vs Cloudfront? | -                                                     |
| Explain AWS S3 Archiving Strategies   | -                                                     |


Domain: CI/CD
| Question                                       | Expectation                         |
|------------------------------------------------|-------------------------------------|
| Explain all stages in a CI/CD Pipeline         | -                                   |
| Explain Deployment Patterns                    | Mention what they are and use cases |
| Explain Jenkinsfile scripted, declarative, DSL | -                                   |

Domain: Containers
| Question                                   | Expectation                 |
|--------------------------------------------|-----------------------------|
| Explain what Docker Stages is what is for? | -                           |
| What are Docker best practices?            | Cover security, lightweight |
| Different ways to expose a service in k8s? | Explain the 3 cases         |
| How to create a package with Helm?         | Go step by step             |


Domain: Containers
| Question                               | Expectation                                               |
|----------------------------------------|-----------------------------------------------------------|
| How to monitor infra with Newrelic?    | Explain installation and how to access data in Newrelic   |
| How Prometheus work?                   | Explain how prometheus stores data and how exporters work |
| What monitoring tools have you worked? | Just mention a list and a brief description               |


Domain: IaaC, CaC, Coding
| Question                                 | Expectation                                               |
|------------------------------------------|-----------------------------------------------------------|
| How Ansible works?                       | Mention how it SSH into servers and how it runs playbooks |
| Elements of an Ansible recipe?           | -                                                         |
| How to create a Terraform Module?        | Mention TF variables, locals, resoruces, data             |
| What is Terraform State?                 | How it is generated, where is stored                      |
| Difference Terraform Variables vs Locals | -                                                         |
| What scripting languages you know?       | Just mention a list and when you used them                |

Domain: Open questions
| Question                                          | Expectation                                                            |
|---------------------------------------------------|------------------------------------------------------------------------|
| What was the most challenging problem you solved? | Explain technically how you solved the problem                         |
| Any question for us?                              | Ask if they need 24/7 on call, Ask how many people and teams they have |

## Others: Behavioural
Some companies have designated people (maybe HR? or Psychologists?) to know you better as a Human being :laughing: - ... just to make sure they are not hiring an Alien or something.
- What are you soft skills?
- How do you see yourself in 3 or 5 years?
- What keeps you motivated to do what you do?
- What you expect in a Company?
- How do you delivery last-minute tasks?
- Did you have any internal problem on any previous job? How did you managed it?
