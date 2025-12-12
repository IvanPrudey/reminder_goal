import asyncio
import os
import time
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logging.error('BOT_TOKEN не найден в .env файле!')
    exit(1)

MSG = '{}, ты сегодня кодил?'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'Пользователь {user_id=} {user_full_name=} запустил бота {time.asctime()}')
    await message.reply(f'Привет, {user_full_name}, я буду напоминать тебе о кодинге!')

    for i in range(7):
        await asyncio.sleep(60*60*24)
        try:
            await bot.send_message(user_id, MSG.format(user_name))
            logging.info(f'Отправлено напоминание в {i+1}/7 дней')
        except Exception as e:
            logging.error(f'Ошибка при отправке сообщения: {e}')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Работа бота завершена')
