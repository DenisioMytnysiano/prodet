import os


class TelegramPublisherConfig:
    TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
    KAFKA_HOST = os.environ.get("KAFKA_HOST")
    KAFKA_PORT = os.environ.get("KAFKA_PORT")
    KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")
