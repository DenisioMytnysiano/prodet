import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_TOPIC = "PropagandaDetector.Messages.Raw"
