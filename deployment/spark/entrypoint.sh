#!/bin/sh
pip install translators spacy_fastlang &&\
python -m spacy download en_core_web_sm &&\
sh -c "/opt/bitnami/spark/sbin/start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.kafka:kafka-clients:3.5.0"
