import aiohttp
from aiogram.types import Message
from main import TOKEN


def clean_and_format_additional_info(additional_info: dict) -> str:
    filtered_info = {k: v for k, v in additional_info.items() if v is not None}
    formatted_info = "\n".join([f"{k}: {v}" for k, v in filtered_info.items()])
    return formatted_info


class ImeiClient:
    @staticmethod
    async def make_request_imei_data(message: Message):
        url = "http://application:8001/api/check-imei"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }
        body = {"imei": message.text}
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
