from aiogram import types
from loader import dp
import utils.db_api.db_handler
from utils.db_api.db_handler import conn, cur
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
# @dp.message_handler(Command('feed'))
# async def process_feed(message: types.Message):
#     cur.execute(
#         'SELECT nickname, school_grade, subjects_user_know, subjects_to_learn FROM users'
#     )
#     data_to_show = cur.fetchall




@dp.message_handler(Command('feed'))
async def process_show_resumes(message: Message):
    cur.execute(
        'SELECT nickname, school_grade, subjects_user_know, subjects_to_learn FROM users'
    )
    global data_to_show
    data_to_show = cur.fetchall()
    
    reply_markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Дальше", callback_data="update_resume")
    )
    try:
        resume = data_to_show.pop()
        await message.answer(f'ник: {resume[0]}, \nгод обучения:{resume[1]}, \nпредметы в которых шарит: {resume[2]}, \nпредметы в которых хочет шарить: {resume[3]}', reply_markup=reply_markup)
    except:
        pass


@dp.callback_query_handler(text="update_resume")
async def resume_update(query: CallbackQuery):
    
    reply_markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Дальше", callback_data="update_resume")
    )
    try:
        resume = data_to_show.pop()
        await query.message.edit_text(f'ник: {resume[0]}, \nгод обучения:{resume[1]}, \nпредметы в которых шарит: {resume[2]}, \nпредметы в которых хочет шарить: {resume[3]}', reply_markup=reply_markup)
    except:
        pass
