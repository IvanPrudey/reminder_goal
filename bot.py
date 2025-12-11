import os
import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.INFO(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f'Привет, {user_full_name}')

if __name__ == '__main__':
    pass
