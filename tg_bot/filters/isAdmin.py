from aiogram.filters import BaseFilter
from aiogram.types import Message
from pydantic import BaseModel
import aiohttp


# Модель для ответа API
class BasicResponse(BaseModel):
    is_succeeded: bool
    additional_info: str


# Фильтр для проверки, является ли пользователь администратором
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        extracted_id = message.from_user.id
        url = f"http://application:8001/api/check-user?telegram_id={extracted_id}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # Проверяем, что запрос успешен
                    json_data = await response.json()  # Декодируем JSON-ответ

                    # Преобразуем JSON в модель BasicResponse
                    api_response = BasicResponse(**json_data)

                    # Проверяем, является ли пользователь администратором
                    if api_response.is_succeeded:
                        return True  # Пользователь администратор
                    else:
                        return False  # Пользователь не администратор

        except aiohttp.ClientError as e:
            print(f"HTTP error occurred: {e}")
            return False  # В случае ошибки считаем, что пользователь не администратор
        except Exception as e:
            print(f"An error occurred: {e}")
            return False  # В случае ошибки считаем, что пользователь не администратор
