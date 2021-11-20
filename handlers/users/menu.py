from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from keyboards.default import menu
from loader import dp



@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("выберите товар ниже: ", reply_markup=menu)


@dp.message_handler(Text(equals=['котлетки', "макарошки", "пюрешка"]))
async def get_food(message: Message):
    await message.answer(f'вы выбрали {message.text}, Спасибо', reply_markup=ReplyKeyboardRemove())
