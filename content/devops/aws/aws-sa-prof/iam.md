# IAM

- curl http://169.256.169.254/latest/meta-data/iam/security-credentials whill show current role
- curl http://169.256.169.254/latest/meta-data/iam/security-credentials/$ROLE_NAME will give current security-credentials

### IAM Boundaries

- Denies the action if something is out of Boundaries
- A separated iam policy just to define Boundaries

### Policy evaluation top-down

1. Explicit deny
2. SCP
3. Resource independent policies
4. Session policies
5. Identity policies

### Tips

- Invalidate existing sessions:
  - Attach an iam role
  - Apply a Revoke Policy based on a date (iam policy conditional)
