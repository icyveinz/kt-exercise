from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from filters.isAdmin import IsAdmin
from filters.isNumeric import IsNumeric
from services.imei import ImeiService

imei_router = Router()

@imei_router.message(CommandStart(), IsAdmin())
async def starting_info(message: Message):
    await ImeiService.start_greetings(message)


@imei_router.message(CommandStart(), ~IsAdmin())
async def starting_decline(message: Message):
    await ImeiService.start_decline(message)


@imei_router.message(IsAdmin(), IsNumeric())
async def check_imei(message: Message):
    await ImeiService.get_imei_info(message)


@imei_router.message(IsAdmin(), ~IsNumeric())
async def check_imei(message: Message):
    await ImeiService.imei_format_error(message)
