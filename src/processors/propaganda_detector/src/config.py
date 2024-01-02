import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_RAW_TOPIC = "Prodet.Messages.Raw"
    KAFKA_TRANSLATED_TOPIC = "Prodet.Messages.Translated"
    KAFKA_PREPARED_TOPIC = "Prodet.Messages.Prepared"
    KAFKA_PROCESSED_TOPIC = "Prodet.Messages.Processed"
    
    SPARK_HOST = os.environ.get("SPARK_HOST")
    SPARK_PORT = os.environ.get("SPARK_PORT")
