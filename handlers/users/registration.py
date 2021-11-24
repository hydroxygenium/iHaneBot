import datetime #to store the user's registration datetime 
import logging
from types import NoneType #for logging
import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from aiogram.types import reply_keyboard
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.types import ParseMode
import data
from keyboards.default import menu
from loader import dp, bot
from utils import db_api
from utils.db_api.db_handler import User


class Form(StatesGroup):
   nickname = State()    # Will be represented in storage as 'Form:nickname'
   school_grade = State()    # Will be represented in storage as 'Form:school_grade'
   subjects_user_know = State()    # Will be represented in storage as 'Form:subjects_user_know'
   subjects_to_learn = State()    # Will be represented in storage as 'Form:subjects_to_learn'


@dp.message_handler(commands='registration')
async def registration_start(message: types.Message):
   """
   Conversation's entry point
   """
   # Set state
   await Form.name.set()

   await message.reply("Твой Никнейм?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
   """
   Allow user to cancel any action
   """
   current_state = await state.get_state()
   if current_state is None:
      return

   logging.info('Cancelling state %r', current_state)
   # Cancel state and inform user about it
   await state.finish()
   # And remove keyboard (just in case)
   await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.nickname)
async def process_nick_name(message: types.Message, state: FSMContext):
   """
   Process user nickname
   """
   async with state.proxy() as data:
      data['nickname'] = message.text

   await Form.next()
   await message.reply("На каком ты году обучения?")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.school_grade)
async def process_school_grade_invalid(message: types.Message):
   """
   If school_grade is invalid
   """
   return await message.rep("Год обучения должен быть числом! Введите снова")

@dp.message_handler(lambda message: message.text.isdigit(), state=Form.school_grade)
async def process_school_grade(message: types.Message, state: FSMContext):
   # Update state and data
   await Form.next()
   await state.update_data(age=int(message.text))

   await message.reply("Предметы в которых ты шаришь? напиши через запятую")

@dp.message_handler(lambda message: len(message.text.split())<=1, state=Form.subjects_user_know)
async def process_subject_user_know_invalid(message: types.Message):
   """
   In this corutine lenth of list of subjects user know has to be greater than or equal to 1
   """
   return await message.reply("Некоректный ввод, поробуйте по другому!")

@dp.message_handler(state=Form.subjects_user_know)
async def process_subjects_user_know(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['subjects_user_know'] = message.text
   
   await Form.next()
   await message.reply("Предметы в которых ты хочешь шарить? Перечисли через запятую.")

@dp.message_handler(lambda message: len(message.text.split())<=1, state=Form.subjects_to_learn)
async def process_subject_to_know_invalid(message: types.Message):
   """
   In this corutine lenth of list of subjects user want to know has to be greater than or equal to 1
   """
   return await message.reply("Некоректный ввод, поробуйте по другому!")

@dp.message_handler(state=Form.subjects_to_know)
async def process_subjects_to_know(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      user_registration_datetime = str(datatime.datetime.now())

      data['subjects_to_know'] = message.text
      # Remove keyboard
      markup = types.ReplyKeyboardRemove()
      
      #for sending it to a db_handler
      user = User(
         datetime.datetime.now,
         data['nickname'],
         data['school_grade'],
         data['subjects_user_know'],
         data['subjects_to_know'],
      )

      # And send message
      await bot.send_message(
         message.chat.id,
         md.text(
            md.text('Твой никнейм: ', md.bold(data['nickname'])),
            md.text('Год обучения: ', md.code(data['school_grade'])),
            md.text('Предметы в которых ты шаришь: ', data['subjects_user_know']),
            md.text('Предметы в которых ты хочешь шарить: ', data['subjects_to_know']),
            sep='\n',
         ),
         reply_markup=markup,
         parse_mode=ParseMode.MARKDOWN,
      )

   # Finish conversation
   await state.finish()
