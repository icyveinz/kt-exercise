import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from routers.imei import imei_router


load_dotenv(".env")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

dp.include_router(router=imei_router)


if __name__ == "__main__":
    dp.run_polling(bot)
