import os
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from filters.isAdmin import IsAdmin
from filters.isNumeric import IsNumeric

def clean_and_format_additional_info(additional_info: dict) -> str:
    filtered_info = {k: v for k, v in additional_info.items() if v is not None}
    formatted_info = "\n".join([f"{k}: {v}" for k, v in filtered_info.items()])
    return formatted_info

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
    extracted_imei = message.text
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    body = {
        "imei": extracted_imei
    }
    url = "http://application:8001/api/check-imei"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as response:
                response.raise_for_status()
                result = await response.json()
                cleaned = clean_and_format_additional_info(result["result"])
                return message.reply(text=cleaned)
    except aiohttp.ClientError as e:
        print(f"HTTP error occurred: {e}")
        return message.reply(text=str(e))
    except Exception as e:
        print(f"An error occurred: {e}")
        return message.reply(text=str(e))


if __name__ == "__main__":
    dp.run_polling(bot)
