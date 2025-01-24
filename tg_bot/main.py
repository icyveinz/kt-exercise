from aiogram import Bot, Dispatcher
from config import Config
from routers.imei import imei_router

bot = Bot(token=Config.TELEGRAM_TOKEN)
dp = Dispatcher()

dp.include_router(router=imei_router)


if __name__ == "__main__":
    dp.run_polling(bot)
