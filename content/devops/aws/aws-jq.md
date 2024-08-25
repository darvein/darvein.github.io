# AWS and JQ Examples

```bash
# List instances by creation time
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,LaunchTime]' --region us-west-2 --output text | sort -n -k 2

# List all EC2 Instances
aws ec2 describe-instances --region us-east-1 \
  | jq -r \
  '.Reservations[].Instances[]
  | [.InstanceId, .PublicIpAddress, (.Tags[]|select(.Key=="Name").Value)]'

aws ec2 describe-instances |\
  jq -r \
  '.Reservations[].Instances[] 
  | select(.Tags[].Key | contains("auto")).PublicIpAddress'

aws rds describe-db-instances |\
  jq -r \
  '.DBInstances[] 
  | select(.Engine=="postgres" and .DBInstanceIdentifier=="acmeorg-eks-apps-production").DBInstanceStatus'

aws ec2 describe-subnets |\
  jq -r \
  '.Subnets[] 
  | {vpc: .VpcId, Subnet: .SubnetId, CIDR: .CidrBlock}'

aws ecr describe-repositories |\ 
  jq -r \
  '.repositories[] 
  | select(.imageScanningConfiguration.scanOnPush==false).repositoryName'

aws ec2 describe-instances --region us-east-2 |\
  jq -r '.Reservations[].Instances[] | select(.Tags[].Value | contains("Jenkins")).InstanceId'

aws ec2 describe-iam-instance-profile-associations --region us-east-2 |\
  jq -r '.IamInstanceProfileAssociations[] | select(.InstanceId=="i-034fd80486cbbdab9")'

aws ec2 describe-iam-instance-profile-associations --region us-east-2 |
  jq -r '.IamInstanceProfileAssociations[] | select(.InstanceId=="i-0896ce482f87185e1")'

aws ec2 describe-vpcs |\
  jq -r '.Vpcs[] | {cidr: .CidrBlock, vpc: .VpcId, tags: .Tags[]}'

aws rds describe-db-instances |\
  jq -r '.DBInstances[] | select(.DBSubnetGroup.VpcId=="vpc-0175ae9e0fd5c227f").DBClusterIdentifier'

aws autoscaling describe-auto-scaling-groups --region us-east-2 |\ 
  jq -r '.AutoScalingGroups[] | select(.AutoScalingGroupName=="admarket")'

aws ec2 describe-subnets --region us-east-2 |\
  jq -r \
  '.Subnets[] 
  | select(.Tags[].Value 
  | contains("Private")) 
  | select(.VpcId == "vpc-0fead42d91a4b1080") 
  | {az: .AvailabilityZone , id: {id: .SubnetId}}' \
  2>/dev/null |\
  jq -r --indent 2 '.az + ":", .id' | sed -e 's/\"//g;'

aws autoscaling --region=us-east-2 describe-auto-scaling-groups |\
  jq -r '.AutoScalingGroups[].Instances[].InstanceId'

aws ec2 describe-instances --filters 'Name=tag:Bastion,Values=true' --region us-east-2 |\
  jq -r '.Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicIp'

INSTID="i-08075f1e6694080d3"; aws ec2 describe-instances --region us-east-2 |\ 
  jq -r \
  ".Reservations[].Instances[] 
  | select(.InstanceId == \"${INSTID}\").PrivateIpAddress"

for x in $(eksctl get cluster -o yaml | yq -r '.[].metadata.name') ; do asg=$(eksctl get nodegroup --cluster ${x} -o json | jq -r '.[].AutoScalingGroupName') ; for i in $(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name ${asg} | jq -r '.AutoScalingGroups[].VPCZoneIdentifier | split(",")' | jq -r '.[0]') ; do aws ec2 describe-subnets --subnet-ids ${i} | jq -r '.Subnets[] | {vpc: .VpcId, Cidr: .CidrBlock}' ; done ; done

aws eks describe-nodegroup --nodegroup-name admarket-production-spot-nodes-autoscaling-group --cluster-name admarket-production-eks |\ 
  jq -r '.nodegroup.health'

while : ; do aws rds describe-db-instances | jq -r '.DBInstances[] | select(.Engine=="postgres" and .DBInstanceIdentifier=="acmeorg-eks-apps-production").DBInstanceStatus' ; sleep 30 ; done

for a in $(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name eks-92c071d0-2d92-d7f7-ccbe-f8c568ea79f7 | jq -r '.AutoScalingGroups[].Instances[].InstanceId') ; do ~/bin/nodeshell $(aws ec2 describe-instances | jq -r ".Reservations[].Instances[] | select(.InstanceId==\"${a}\").PrivateDnsName") ; done

for a in $(aws ec2 describe-instances | jq -r '.Reservations[].Instances[] | select(.Tags[].Value | test("[Jj]enkins")) | [.PrivateDnsName,.SecurityGroups[].GroupId] |@csv') ;do echo -e "\n${a}\n" ; sleep 1 ;  aws ec2 describe-security-group-rules --filter Name="group-id",Values="$(echo ${a} | cut -f 2 -d ',')" | jq -r '.SecurityGroupRules[] | {ip: .IpProtocol, egress: .IsEgress, from: .FromPort, to: .ToPort, cidr: .CidrIpv4}'; done

for i in i-05363557d57e03c45 i-0b4ddb7579307b031 ; do aws ec2 describe-instances | jq -r ".Reservations[].Instances[] | select(.InstanceId==\"${i}\").PrivateIpAddress" ; done

# List route53 all subdomains
for zone in `aws route53 list-hosted-zones | jq -r '.HostedZones[].Id'`; do \
    aws route53 list-resource-record-sets --hosted-zone-id $zone |\
    jq -r '.ResourceRecordSets[]? | "\(.Name),\(.Type),\(.ResourceRecords[]?.Value)"'; \
done
```

## More JQ Examples

```bash
# get key name of ec2 box
aws ec2 describe-instances --instance-ids i-0e2x8xd7xxx | jq '.Reservations[].Instances[].KeyName'


# Parse big JSON output with jq
aws --profile efsociety ec2 describe-instances --output json | jq '.Reservations[] | .Instances[] | [ (.Tags[]|select(.Key=="Name").Value), .InstanceType, .InstanceId, .State.Name]'

# Example of Cloudformation execution 
aws --profile $AWS_PROFILE --region $AWS_REGION cloudformation update-stack \
	--stack-name dcg-vpc-lambda \
	--template-body  [file://vpc-nat-eip.json](file:///vpc-nat-eip.json)  \
	--parameters ParameterKey=Project,ParameterValue=$PROJ_NAME \
	ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
	ParameterKey=VpcCIDR,ParameterValue=$VPC_CIDR \
	ParameterKey=PublicSubnet1Param,ParameterValue=$PUBLIC_SUBNET \
	ParameterKey=PrivateSubnet1Param,ParameterValue=$PRIVATE_SUBNET \
	ParameterKey=SGPortIngress,ParameterValue=$SG_PORT_IN


aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --output=text

# tabbed output: tag name, instance id and private ip addr
aws  --region us-west-2 ec2 describe-instances --output json | jq -r '.Reservations[] | .Instances[] | "\(.Tags[]|select(.Key=="Name").Value)\t\(.InstanceId)\t\(.PrivateIpAddress)"'
```

### How to merge two JQ outputs, merge JSON objs

```bash
jq -n \
	--arg url $JENKINS_URL \
	--arg author $JENKINS_AUTHOR \
	--arg date $JENKINS_DATE \
	'{"url": $ARGS.named["url"], "author": $ARGS.named["author"], "date": $ARGS.named["date"]}' > jenkins_info.json

jq -n \
	--arg db_schema $DB_SCHEMA \
	--arg branch $BRANCH \
	--arg environment $ENVIRONMENT \
	--arg environment_instance $ENVIRONMENT_INSTANCE \
	--arg automated $AUTOMATED \
	'{"db_schema": $ARGS.named["db_schema"], "branch": $ARGS.named["branch"], "environment": $ARGS.named["environment"], "environment_instance": $ARGS.named["environment_instance"], "automated": $ARGS.named["automated"]}' > deployment_info.json

jq --argjson jenkinsInfo "$(<jenkins_info.json)" '.jenkins_info = $jenkinsInfo' deployment_info.json > AlumniDbSchema.json

# Secrets
aws secretsmanager list-secrets | jq '.SecretList[] | [.Name, .Tags]'
```

### More examples
- https://gist.github.com/lukeplausin/b64c10f8b524bb310e0083756c42caf6
