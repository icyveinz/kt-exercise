from aiogram.types import Message
from clients.imei import ImeiClient
from main import TOKEN


class ImeiService:
    @staticmethod
    async def start_greetings(message: Message):
        await message.answer(
            text="Этот бот поможет получить информацию о IMEI.\nВведите в поле интересующий вас IMEI (последовательность из 15 цифр)"
        )

    @staticmethod
    async def start_decline(message: Message):
        await message.answer(text="У вас нет доступа к данному боту")

    @staticmethod
    async def imei_format_error(message: Message):
        await message.answer(
            text="Проверьте номер, который вы отправили. Он должен состоять из 15 цифр и не должен содержать других символов"
        )

    @staticmethod
    async def get_imei_info(message: Message):
        extracted_imei = message.text
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }
        body = {"imei": extracted_imei}
        return await ImeiClient.make_request_imei_data(message, headers, body)
