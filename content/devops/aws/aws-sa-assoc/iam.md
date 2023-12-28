# Identity Access Management

## Generalities

- Root account shouldn't be used for shopping. First account when you create an AWS Account
- AWS Accounts created by a single Root user are isolated and secure
- Each account handles: Authentication, Authorization and Billing individually
- Objs: 
  - Users
  - Groups
  - Roles
  - Permissions (policies)
- Security principles: Authentication & Authorization
- Chain of credentials https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/DefaultAWSCredentialsProviderChain.html

## Generalities v2

- Root
- Users/User Groups
    - Groups: Administrators, Devops, Developers, Externals ("readonly")
    - Users: regular users for people!, service accounts (iam user for github actions)
      - Administrator User
        - Adminstrator user doens't have access to Billing/Costs
- Roles
    - For aws services: ec2, ecs/eks, asg, lambdas
      - EC2 Instance Profile
    - SSM (AWS System Manager)
    - KMS/HSM? (Key Management Service)
- Policies
  - IAM Policy best practices
- IdP (identity provider)
    - AWS Cognito
    - OpenSAML
- Cloudwatch & Cloudtrail
    - See who got access and authentication
- Organizations

## Users

  ### good practice
  - all users need to activate MFA, specially the root acct.
  - pasword rotation policies has to be enabled for everyone
  - the root aws account shouldn't be used for operations
  - new user ha no permissions when first created

## Roles
Types:
- AWS service role
- AWS service-linked role
- Role for cross-account access
- Role for identity provider access

## Groups

## Policies

## References

- aws organizations: https://docs.aws.amazon.com/organizations/latest/userguide/organizations-userguide.pdf
- iam policies in a nutshell: https://start.jcolemorrison.com/aws-iam-policies-in-a-nutshell/
- iam policy variables: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html
