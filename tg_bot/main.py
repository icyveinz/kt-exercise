import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from filters.isAdmin import IsAdmin
from filters.isNumeric import IsNumeric

load_dotenv(".env")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TOKEN = os.getenv("TOKEN")

print(TELEGRAM_TOKEN)
print(TOKEN)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart(), IsAdmin())
async def starting_info(message: Message):
    await message.answer(
        text="Этот бот поможет получить информацию о IMEI.\nВведите в поле интересующий вас IMEI (последовательность из 15 цифр)"
    )


@dp.message(CommandStart(), ~IsAdmin())
async def starting_info(message: Message):
    await message.answer(text="У вас нет доступа к данному боту")


@dp.message(IsAdmin(), IsNumeric())
async def check_imei(message: Message):
    extracted_imei = int(message.text)
    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }


if __name__ == "__main__":
    dp.run_polling(bot)
