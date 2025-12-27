"""Обработчик команды /start"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start"""
    await message.answer(
        "Привет! 👋\n\n"
        "Задайте свой вопрос, и я постараюсь на него ответить."
    )



