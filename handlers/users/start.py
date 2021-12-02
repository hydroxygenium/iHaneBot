from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = f"""
Привет, {message.from_user.full_name}!
Этот бот пока что полностью не готов.

В нем сечас можно делать 2 вещи:
    Регистрироваться /registration
    Просматривать ленту анкет /feed
"""
    await message.answer(text)
