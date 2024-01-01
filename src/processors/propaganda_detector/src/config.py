import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_RAW_TOPIC = "PropagandaDetector.Messages.Raw"
    KAFKA_TRANSLATED_TOPIC = "PropagandaDetector.Messages.Translated"
    KAFKA_PREPARED_TOPIC = "PropagandaDetector.Messages.Prepared"
    KAFKA_PROCESSED_TOPIC = "PropagandaDetector.Messages.Processed"
    SPARK_HOST = os.environ.get("SPARK_HOST")
    SPARK_PORT = os.environ.get("SPARK_PORT")

print(Config.__dict__)