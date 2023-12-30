import os


class TelegramPublisherConfig:
    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")
