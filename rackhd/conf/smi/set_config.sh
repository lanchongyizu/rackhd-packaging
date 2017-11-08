#!/bin/bash
curl -XPUT -H "Content-Type:text/plain" localhost:8500/v1/kv/config/DEVICE-DISCOVERY/data --data-binary @- < ./device-discovery.yml
curl -XPUT -H "Content-Type:text/plain" localhost:8500/v1/kv/config/virtualnetwork/data --data-binary @- < ./virtualnetwork.yml
curl -XPUT -H "Content-Type:text/plain" localhost:8500/v1/kv/config/virtualidentity/data --data-binary @- < ./virtualidentity.yml
curl -XPUT -H "Content-Type:text/plain" localhost:8500/v1/kv/config/gateway-zuul/data --data-binary @- < ./gateway.yml
curl -XPUT -H "Content-Type:text/plain" localhost:8500/v1/kv/config/SWAGGER-AGGREGATOR/data --data-binary @- < ./swagger-aggregator.yml
