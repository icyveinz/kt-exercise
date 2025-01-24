from aiogram.filters import BaseFilter
from aiogram.types import Message
from pydantic import BaseModel
import aiohttp

class BasicResponse(BaseModel):
    is_succeeded: bool
    additional_info: str


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        extracted_id = message.from_user.id
        url = f"http://application:8001/api/check-user?telegram_id={extracted_id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    api_response = BasicResponse(**json_data)
                    if api_response.is_succeeded:
                        return True
                    else:
                        return False

        except aiohttp.ClientError as e:
            print(f"HTTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
