import json
import uuid
from confluent_kafka import Producer, Message

from .config import Config


producer = Producer({
    "bootstrap.servers": f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
})

async def produce_message_to_kafka(message: dict[str, str]) -> None:
    print(f"Received the message: {message}")
    producer.produce(Config.KAFKA_TOPIC,
                     key=str(uuid.uuid4()),
                     value=json.dumps(message),
                     on_delivery=on_kafka_produce)
    producer.poll(0)

def on_kafka_produce(err: str, message: Message) -> None:
    if err is not None:
        print(f"Failed produce to the message: {err}")
    else:
        print(f"Produced the message: id={message.key()}")
