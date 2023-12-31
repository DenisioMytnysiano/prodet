import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_RAW_TOPIC = "PropagandaDetector.Messages.Raw"
    KAFKA_PREPARED_TOPIC = "PropagandaDetector.Messages.Prepared"

    SPARK_HOST = os.environ.get("SPARK_HOST")
    SPARK_PORT = os.environ.get("SPARK_PORT")

    ELASTIC_HOST = os.environ.get("ELASTIC_HOST")
    ELASTIC_PORT = os.environ.get("ELASTIC_PORT")
