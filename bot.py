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

active_users = {}


@dp.message(Command('start'))
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'Пользователь {user_id=} {user_full_name=} запустил бота {time.asctime()}')
    await message.reply(f'Привет, {user_full_name}, я буду напоминать тебе о кодинге!')
    asyncio.create_task(send_reminders(user_id, user_name))


async def send_reminders(user_id: int, user_name: str):
    try:
        for i in range(7):
            await asyncio.sleep(60)
            # await asyncio.sleep(60*60*24)
            try:
                await bot.send_message(user_id, MSG.format(user_name))
                logging.info(f'Отправлено напоминание в день {i+1}/7 пользователю {user_name}')
            except Exception as e:
                logging.error(f'Ошибка при отправке сообщения: {e}')
                break
        logging.info(f'Напоминания завершены для пользователя {user_name}')
        await bot.send_message(user_id, f'{user_name}, неделя напоминаний завершена!')
    except asyncio.CancelledError:
        logging.info(f'Напоминания отменены для пользователя {user_name}')
    except Exception as e:
        logging.error(f'Ошибка в задаче напоминаний: {e}')


@dp.message(Command('stop'))
async def stop_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if user_id in active_users:
        await message.reply(f'{user_name}, напоминания остановлены!')
    else:
        await message.reply(f'{user_name}, у Вас нет активных напоминаний.')


async def main():
    logging.info('Запуск бота...')
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info('Бот остановлен пользователем')
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Работа бота завершена')
