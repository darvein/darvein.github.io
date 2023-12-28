# Elasticsearch cheatsheet


```bash
export HST=https://elasticsearch.devbox-apps.acme.com

# see why not allocate shareds
curl -s -XGET localhost:9200/_cluster/allocation/explain?pretty

# check unallocated shareds
curl -s -XGET localhost:9200/_cat/shards?

# check installed plugins
curl -X GET "localhost:9200/_cat/plugins?v&s=component&h=name,component,version,description&pretty"

# check ES health
curl -sX GET "$HST/_cluster/health" | jq
curl -sX GET "https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_cluster/health" | jq

# stats
curl -X GET "localhost:9200/_nodes/stats" | jq
curl -X GET "localhost:9200/_nodes/stats/indices" | jq
curl -X GET "http://localhost:9200/_stats?all=true" | jq

# List indexes
curl -s "$HST/_aliases?pretty=true" | jq
curl -s "$HST/_cat/indices?v"

# Snapshots
curl -sX GET "$HST/_snapshot/_all?pretty" | jq
curl -sX GET "$HST/_snapshot/_status" | jq

# List taken snapshots from a repository "s3_repository
curl -sX GET "$HST/_snapshot/s3_repository/_all?pretty" | jq

# Check existing snapshots from the repo "backups"
curl -sX GET "$HST/_snapshot/backups/_all" | jq

# Check if data re-indexing is needed
curl -sX GET "$HST/_xpack/migration/deprecations" | jq
```

Troubleshooting

```bash
k delete pod $(k get pods | grep elastic | cut -d ' ' -f1)
k logs -f $(k get pods | grep elastic | cut -d ' ' -f1)
k exec -it $(k get pods | grep elastic | cut -d ' ' -f1) -- cat /usr/share/elasticsearch/config/elasticsearch.yml
```


#### Delete indexes

```bash
# look for indexes
curl -s 'localhost:9200/_cat/indices?v' | awk '{print $3}' | sort | uniq | grep 2019

# delete them
curl -X DELETE localhost:9200/fluentd.service.nginx.conaff.201904w13

curl -X DELETE localhost:9200/
```


Sample

```bash
druiz@drweb0:~/infra-mainsite/containers/elastic$ curl -xX GET "localhost:9200/_cluster/health" | jq
{
  "cluster_name": "logstorage",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 4,
  "number_of_data_nodes": 4,
  "active_primary_shards": 275,
  "active_shards": 550,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100
}

```

#### ES migration to AWS S3

```bash
docker exec -it elastic elasticsearch-plugin install -b repository-s3

curl -X PUT "localhost:9200/_snapshot/msops_s3_repository" -H 'Content-Type: application/json' -d '
{
  "type": "s3",
  "settings": {
	"bucket": "msops-es-snaphosts",
	"region": "us-west-2",
	"role_arn": "arn:aws:iam::539374710386:role/msops-msops-es-snapshot"
  }
}'

curl -X PUT "localhost:9200/_snapshot/msops_s3_repository" -H 'Content-Type: application/json' -d '
{
  "type": "s3",
  "settings": {
	"bucket": "msops-es-snaphosts",
	"region": "us-west-2"
  }
}'

export AWS_ACCESS_KEY_ID=XXX
export AWS_SECRET_ACCESS_KEY=XXXt
export AWS_DEFAULT_REGION=us-west-2

aws sts assume-role --role-arn arn:aws:iam::539374710386:role/msops-msops-es-snapshot --role-session-name es-access-snapshots

```



#### Import s3 data into AWS ES

```bash
# 1. Confirm ES cluster is healthy
curl -sX GET "https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_cluster/health" | jq


# 2. Register a s3 repository with this python script
import boto3
import requests
from requests_aws4auth import AWS4Auth

service = 'es'
region = 'us-west-2'
host = 'https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

path = '_snapshot/msops_s3_repository'
url = host + path
payload = {
  "type": "s3",
  "settings": {
    "bucket": "msops-es-snaphosts",
    "region": "us-west-2",
    "role_arn": "arn:aws:iam::539374710386:role/msops-msops-es-snapshot"
  }
}

headers = {"Content-Type": "application/json"}
r = requests.put(url, auth=awsauth, json=payload, headers=headers)
print(r.status_code)
print(r.text)


# 3. Get a list of snapshots

curl -sXGET 'https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_snapshot/msops_s3_repository/_all' | jq '.snapshots[] | .snapshot' | sort | uniq

"ulelasticsearch-4k1ph9setpipm1sjt932lw"
"ulelasticsearch-5mlthcq2qmmggwyr-bok9g"
"ulelasticsearch-h4ufg-krqek5teqak8-jqg"
"ulelasticsearch-hitvacvrtbmydy5uoa9goq"
"ulelasticsearch-hwjyw-qtq02iafhbhlfdxq"
"ulelasticsearch-km9yfbsrq3-3ph5xufoxzq"
"ulelasticsearch-rwckzs5-rcoslwww9eahtw"
"ulelasticsearch-vy9slvnhqvimssdqu1wy9q"
"ulelasticsearch-wmsnb1a1t-q-ko25l2i3ia"
"ulelasticsearch-wnmr6o6gsqgkitreaqdvsq"
"ulelasticsearch-wsk_7lwzt1ckwcvy6-agkw"
"ulelasticsearch-xekf645gqoa2l6bprc9gla"
"ulelasticsearch-y1qzbanqscuq3i9emren_g"
"ulelasticsearch-yynzapuwq4edw7ab24f_gq""

# 4. Restore each snapshot version

curl -sXPOST 'https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_snapshot/msops_s3_repository/ulelasticsearch-xekf645gqoa2l6bprc9gla/_restore' -d '{"indices": "-.kibana*,-.reporting*,fluentd*", "ignore_unavailable": true, "include_global_state": false, "include_aliases": false}' -H 'Content-Type: application/json'

# 5. Check status
curl -sX GET "https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_snapshot/_all" | jq
curl -sX GET "https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_snapshot/_status" | jq

# 6. Check indices are there and have data
curl "https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/_aliases" | jq

curl "https://vpc-msops-es-cluster-edwk7ppi4dw5gkcpqbqangmbvm.us-west-2.es.amazonaws.com/fluentd.service.nginx.bm2.202002w07/_search" | jq


# CHECK PROBLEMS
https://aws.amazon.com/premiumsupport/knowledge-center/elasticsearch-kibana-error/
https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html
```



## Send CA django logs to ES

1. Update logforwarder and logaggregator in order to receive and process django logs
2. Parse logs format in logforwarder
3. Register the new fluentd index in Kibana



Experiments

```bash
docker run \
	--log-driver=fluentd \
	--log-opt tag='docker.{{.ID}}' \
	--log-opt fluentd-address=localhost:24224 \
	ubuntu echo 'PArt 12'
	

```



## in the logforwarder on fluentd side 

```bash
# gem install fluent-plugin-concat

<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter docker.**>
  @type concat
  key log
  stream_identity_key container_id
  use_first_timestamp true
  multiline_start_regexp /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})[^\s]+/
  #flush_interval 1s
  #timeout_label @NORMAL
</filter>


<match docker.**>
  @type forward
  @id out_aggregator_docker
  transport                          tls
  tls_version                        TLSv1_2
  tls_cert_path                      /fluentd/etc/ssl/ca.crt
  tls_client_cert_path               /fluentd/etc/ssl/client.crt
  tls_client_private_key_path        /fluentd/etc/ssl/client.key
  tls_client_private_key_passphrase  XczdNe]2EKiQhAh/4WfxwH7vpvP8sFMx3TWPCTpFjmv7.Qt2EvN
  tls_verify_hostname                false
  <server>
    host 10.200.36.10
    port 23300
  </server>
  <server>
    host 10.200.36.12
    port 23300
    standby
  </server>
</match>
```



## django ca qa

```bash
docker run \
	--log-driver=fluentd \
	--log-opt tag='docker.{{.ID}}' \
	--log-opt fluentd-address=localhost:24224 \
	-d --label=label.dd-important=true --init --restart=unless-stopped -e DISABLE_NEWRELIC=true --ip=172.22.0.50 --publish 8000:8000 --add-host www.cnsmeraffs.com:10.192.38.101 --add-host docsim.ca:10.192.36.102 -h django-ca-qa-qa0 --net=web --name django-ca-qa -e NEW_RELIC_LICENSE_KEY=a5f3704c3045218f30dd6d899aa97e25b143862d -e NEW_RELIC_ENVIRONMENT=qa -e NEW_RELIC_CONFIG_FILE=/etc/newrelic/newrelic.ini -e MYSQL_CONFIG=qa -e REDIS_CONFIG=qa -e STATSD_SERVER=10.192.38.101 -e CONTAINER_ENVIRONMENT=qa -v /nfsshare02/conaff:/var/www/conaff -v /nfsshare02/exports:/var/www/exports -v logvolume:/var/log/ harbor.cnsmeraffs.com/ca/django-ca:br-qa-3bb4dac-py3 django
	
	
docker stop django-ca-qa
docker rm django-ca-qa

docker run -d --label=label.dd-important=true --init --restart=unless-stopped -e DISABLE_NEWRELIC=true --ip=172.22.0.50 --publish 8000:8000 --add-host www.cnsmeraffs.com:10.192.38.101 --add-host docsim.ca:10.192.36.102 -h django-ca-qa-qa0 --net=web --name django-ca-qa -e NEW_RELIC_LICENSE_KEY=a5f3704c3045218f30dd6d899aa97e25b143862d -e NEW_RELIC_ENVIRONMENT=qa -e NEW_RELIC_CONFIG_FILE=/etc/newrelic/newrelic.ini -e MYSQL_CONFIG=qa -e REDIS_CONFIG=qa -e STATSD_SERVER=10.192.38.101 -e CONTAINER_ENVIRONMENT=qa -v /nfsshare02/conaff:/var/www/conaff -v /nfsshare02/exports:/var/www/exports -v logvolume:/var/log/ harbor.cnsmeraffs.com/ca/django-ca:br-qa-3bb4dac-py3 django
```



### logging to AWS ES

```bash
# fluentd forwarder fluent.conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter docker.**>
  @type concat
  key log
  stream_identity_key container_id
  use_first_timestamp true
  multiline_start_regexp /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})[^\s]+/
  #flush_interval 1s
  #timeout_label @NORMAL
</filter>

<match **>
  @type elasticsearch
  type_name fluentd
  logstash_format true
  logstash_prefix staging
  include_tag_key true
  tag_key @log_name
  host vpc-global-es-vj2klfzx4acdwvtw6sjwacapsi.us-west-2.es.amazonaws.com
  port 443
  scheme https
  ssl_version TLSv1_2
  reload_connections false
  log_es_400_reason true
</match>




# fluentd container
docker stop fluentd
docker rm fluentd
docker run \
	--name fluentd \
	-d \
	-p 24224:24224 -p 24224:24224/udp \
	-v /home/ubuntu/fluentd:/fluentx \
	-v /home/ubuntu/datacnt:/fluentx/log \
	32c0c555eb19 \
	/fluentx/etc/start.sh
	
# fluentd command
#!/bin/sh
gem install fluent-plugin-elasticsearch
gem install fluent-plugin-aws-elasticsearch-service
exec fluentd -c /fluentx/etc/$FLUENTD_CONF -p /fluentx/plugins $FLUENTD_OPT


# test ES
curl -sX GET "https://vpc-global-es-vj2klfzx4acdwvtw6sjwacapsi.us-west-2.es.amazonaws.com/_cluster/health"
```
