import asyncio
import json
import uuid
from aiogram import Bot, Dispatcher, types
from confluent_kafka import Producer
from config import TelegramPublisherConfig
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
producer = Producer({ "bootstrap.servers": f"{TelegramPublisherConfig.KAFKA_HOST}:{TelegramPublisherConfig.KAFKA_PORT}"})
bot = Bot(token=TelegramPublisherConfig.TELEGRAM_API_KEY)
dp = Dispatcher()

def delivery_report(err, msg):
    if err is not None:
        print(f"Failed to produce message. Error:{err}")
    else:
        print("Message delivered successfully")


async def produce_message_to_kafka(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    message_text = message.text
    print(f"User: {username} ({user_id}), Chat: {chat_id}, Message: {message_text}")
    message = {
        "user_id": user_id,
        "user_name": username,
        "chat_id": chat_id,
        "text": message_text,
    }
    producer.produce(
        TelegramPublisherConfig.KAFKA_TOPIC,
        key=str(uuid.uuid4),
        value=json.dumps(message),
        on_delivery=delivery_report
    )
    producer.poll(0)


@dp.message(lambda message: message.text and not message.text.startswith("/"))
async def handle_text_messages(message: types.Message):
    await produce_message_to_kafka(message)


@dp.message(lambda message: message.text and message.text.startswith("/start"))
async def handle_start(message: types.Message):
    await message.reply("Bot is running!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
