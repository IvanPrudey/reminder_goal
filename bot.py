import asyncio
import os
import time
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
MSG = '{}, ты сегодня кодил?'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f'Привет, {user_full_name}')

    for i in range(10):
        await asyncio.sleep(2)
        await bot.send_message(user_id, MSG.format(user_name))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
