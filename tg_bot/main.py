import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv("/.env")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()