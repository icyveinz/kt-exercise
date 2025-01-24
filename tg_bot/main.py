import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from filters.isAdmin import IsAdmin

load_dotenv("/.env")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart() and IsAdmin())
async def starting_info(message: Message):
    await message.answer(
        text="Этот бот поможет получить информацию о IMEI.\nВведите в поле интересующий вас IMEI (последовательность из 15 цифр)"
    )


@dp.message(CommandStart() and not IsAdmin())
async def starting_info(message: Message):
    await message.answer(text="У вас нет доступа к данному боту")


if __name__ == "__main__":
    dp.run_polling(bot)
