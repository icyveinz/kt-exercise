from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsNumeric(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text and message.text.isdigit() and len(message.text) == 15
