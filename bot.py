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
    if user_id in active_users:
        await message.reply(f'{user_full_name}, у тебя уже есть активные напоминания! Используй /stop чтобы остановить их.')
        return
    await message.reply(f'Привет, {user_full_name}, я буду напоминать тебе о кодинге!')
    task = asyncio.create_task(send_reminders(user_id, user_name))
    active_users[user_id] = {
        'task': task,
        'user_name': user_name
    }
    logging.info(f'Создана задача напоминаний для пользователя {user_name} (ID: {user_id})')


async def send_reminders(user_id: int, user_name: str):
    try:
        for i in range(7):
            await asyncio.sleep(60)
            # await asyncio.sleep(60*60*24)
            if user_id not in active_users:
                logging.info(f'Задача напоминаний прервана для пользователя {user_name}')
                return
            try:
                await bot.send_message(user_id, MSG.format(user_name))
                logging.info(f'Отправлено напоминание в день {i+1}/7 пользователю {user_name}')
            except Exception as e:
                logging.error(f'Ошибка при отправке сообщения: {e}')
                if user_id in active_users:
                    del active_users[user_id]
                break
        logging.info(f'Напоминания завершены для пользователя {user_name}')
        await bot.send_message(user_id, f'{user_name}, неделя напоминаний завершена!')
    except asyncio.CancelledError:
        logging.info(f'Напоминания отменены для пользователя {user_name}')
        await bot.send_message(user_id, f'{user_name}, напоминания остановлены!')
    except Exception as e:
        logging.error(f'Ошибка в задаче напоминаний для {user_name}: {e}')
    finally:
        if user_id in active_users:
            del active_users[user_id]


@dp.message(Command('stop'))
async def stop_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if user_id in active_users:
        user_data = active_users[user_id]
        task = user_data['task']
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        await message.reply(f'{user_name}, напоминания остановлены!')
        logging.info(f'Напоминания остановлены для пользователя {user_name}')
    else:
        await message.reply(f'{user_name}, у тебя нет активных напоминаний.')


@dp.message(Command('status'))
async def status_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if user_id in active_users:
        user_data = active_users[user_id]
        task = user_data['task']
        if task.done():
            status = "завершены"
            del active_users[user_id]
        elif task.cancelled():
            status = "отменены"
        else:
            status = "активны"
        await message.reply(f'{user_name}, твои напоминания {status}!')
        logging.info(f'Пользователь {user_name} запросил статус: напоминания {status}')
    else:
        await message.reply(f'{user_name}, у тебя нет активных напоминаний! Используй /start для начала.')
        logging.info(f'Пользователь {user_name} запросил статус: напоминаний нет')


async def main():
    logging.info('Запуск бота...')
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info('Бот остановлен пользователем')
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')
    finally:
        logging.info('Отмена всех активных задач...')
        for user_id, user_data in list(active_users.items()):
            task = user_data['task']
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Работа бота завершена')
