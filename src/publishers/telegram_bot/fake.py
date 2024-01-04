import uuid
import random
import datetime
import asyncio
from faker import Faker
from src.kafka import produce_message_to_kafka

FILE_PATH = "../../../data/files/ukrainian-news.raw.csv"
NETWORK_TYPES = ["facebook", "twitter", "telegram", "instagram"]
FAKER = Faker()

def load_sample_texts():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()[1:5000]]
    
def create_fake_data(text):
    return {
        "id": str(uuid.uuid4()),
        "network_type": random.choice(NETWORK_TYPES),
        "user_id": str(uuid.uuid4()),
        "user_name": FAKER.simple_profile()['username'],
        "chat_id": str(uuid.uuid4()),
        "chat_type": "group",
        "chat_name": str(uuid.uuid4()),
        "text": text,
        "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randrange(0, 30))).isoformat()
    }

async def run(fake_texts: list[str]) -> None:
    for text in fake_texts:
        await produce_message_to_kafka(text)

if __name__ == '__main__':
    texts = load_sample_texts()
    fake_texts = [create_fake_data(text) for text in texts]
    asyncio.run(run(fake_texts))

  
