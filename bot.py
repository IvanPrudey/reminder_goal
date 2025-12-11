import os
import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

if __name__ == '__main__':
    pass
