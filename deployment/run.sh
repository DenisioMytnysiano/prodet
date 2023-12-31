#!/bin/sh

docker compose -f docker-compose-kafka.yml -f docker-compose-spark.yml -f docker-compose-elastic.yml down
docker compose -f docker-compose-kafka.yml -f docker-compose-spark.yml -f docker-compose-elastic.yml up
