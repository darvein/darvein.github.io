# Directory Service

### SSO / SAML 2.0

- AWS can talk SAML2.0 from external IdPs if the SAML Assertion to be send to AWS is correct then AWS provides temporal AWS Creds (AWS STS)
- AD Federated users -> AWS SSO -> Dropbox, Slack, Salesforce... or SAML Apps

### Ad Connector

- AD endpoints injected in a VPC via ENIs
- Uses an existing on-prem AD
- Multiple AD connections to speed and distribute load
- Requieres at least 2 subnets
- Supports network to VPN or Direct Connect
- Ideally works as PoC or backup for a Direct Connect
- Nothing is stored or acched, it just redirects AD traffic to on-prem AD servers
- Network becomes a single point of failure

### Microsoft Managed AD

- Microsoft 2012 R2
- Managed using standard AD Tools
- Standard: 30k users, Enterprise: 5000k Users
- Radius-base MFA support
- By default support HA
- Support 1-way or 2-way trust (with on-prem)
- Supports AD Native scheme extensions

### Simple AD

- ?
