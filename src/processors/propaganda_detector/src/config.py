import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.13:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0 pyspark-shell'

class Config:
    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_RAW_TOPIC = "PropagandaDetector.Messages.Raw"
    KAFKA_PREPARED_TOPIC = "PropagandaDetector.Messages.Prepared"

    SPARK_HOST = os.environ.get("SPARK_HOST")
    SPARK_PORT = os.environ.get("SPARK_PORT")

    ELASTIC_HOST = os.environ.get("ELASTIC_HOST")
    ELASTIC_PORT = os.environ.get("ELASTIC_PORT")
