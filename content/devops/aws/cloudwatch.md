# AWS Cloudwatch

```sql
# insights LE dry-run

fields @timestamp, @logStream, @message
  | filter @message like /The dry run was successful/

fields @timestamp, @logStream, @message
  | filter @message like /The following errors were reported by the server/

fields @timestamp, @logStream, @message
  | filter @message like /ALB is not ready after 200 tries/


# insights LE real

fields @timestamp, @logStream, @message
  | filter @message like /Your certificate and chain have been saved at/

fields @timestamp, @logStream, @message
  | filter @message like /unauthorized/

fields @timestamp, @logStream, @message
  | filter @message like /Exception/
```
