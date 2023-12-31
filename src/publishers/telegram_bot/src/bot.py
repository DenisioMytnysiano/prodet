from aiogram import Bot, Dispatcher, types

from .config import Config
from .kafka import produce_message_to_kafka


bot = Bot(token=Config.TELEGRAM_API_KEY)
dp = Dispatcher()

def map_message_to_dict(message: types.Message) -> dict[str, str]:
    return {
        "id": message.message_id,
        "network_type": "telegram",
        "user_id": message.from_user.id,
        "user_name": message.from_user.username,
        "chat_id": message.chat.id,
        "chat_type": message.chat.type,
        "chat_name": message.chat.username or message.chat.title,
        "text": message.text,
        "created_at": message.date.isoformat()
    }

@dp.message(lambda message: message.text and not message.text.startswith("/"))
async def handle_text_messages(message: types.Message):
    message_dict = map_message_to_dict(message)
    await produce_message_to_kafka(message_dict)

@dp.message(lambda message: message.text and message.text.startswith("/start"))
async def handle_start(message: types.Message):
    await message.reply("Bot is running!")

async def init_bot():
    await dp.start_polling(bot)
