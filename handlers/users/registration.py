import datetime #to store the users registration datetime 
import logging
import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ParseMode
# import data
from loader import dp, bot
from utils.db_api.db_handler import *


class Form(StatesGroup):
    """
    Data class for user registration
    """
    # Will be represented in storage as 
    nickname = State()    #'Form:nickname'
    school_grade = State()    # 'Form:school_grade'
    subjects_user_know = State()    # 'Form:subjects_user_know'
    subjects_to_learn = State()    # 'Form:subjects_to_learn'


@dp.message_handler(Command('registration'))
async def registration_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.nickname.set()
    questiontext = "Твой Никнейм?"
    await message.reply(questiontext)


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
    questiontext = "На каком ты году обучения?"
    await message.reply(questiontext)


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.school_grade)
async def process_school_grade_invalid(message: types.Message):
    """
    If school_grade is invalid
    """
    error_text = "Год обучения должен быть числом! Введите снова"
    return await message.reply(error_text)

@dp.message_handler(lambda message: message.text.isdigit(), state=Form.school_grade)
async def process_school_grade(message: types.Message, state: FSMContext):
    """
    process school grade
    """
    # Update state and data

    # await state.update_data(school_grade=int(message.text))
    async with state.proxy() as data:
        data['school_grade'] = message.text

    await Form.next()
    questiontext = "Предметы в которых ты шаришь? напиши через запятую"
    await message.reply(questiontext)

@dp.message_handler(lambda message: len(message.text.split())<=1, state=Form.subjects_user_know)
async def process_subject_user_know_invalid(message: types.Message):
    """
    In this corutine lenth of list of subjects user know has to be greater than or equal to 1
    """"Некоректный ввод, поробуйте по другому!"
    error_text = "Некоректный ввод, поробуйте по другому!"
    return await message.reply(error_text)

@dp.message_handler(state=Form.subjects_user_know)
async def process_subjects_user_know(message: types.Message, state: FSMContext):
    """
    process subjects user know
    """
    async with state.proxy() as data:
        data['subjects_user_know'] = message.text

    await Form.next()
    questiontext = "Предметы в которых ты хочешь шарить? Перечисли через запятую."
    await message.reply(questiontext)

@dp.message_handler(lambda message: len(message.text.split())<=1, state=Form.subjects_to_learn)
async def process_subject_to_know_invalid(message: types.Message):
    """
    In this corutine lenth of list of subjects
    user want to know has to be greater than or equal to 1
    """
    error_text = "Некоректный ввод, попробуйте по другому!"
    return await message.reply(error_text)

@dp.message_handler(state=Form.subjects_to_learn)
async def process_subjects_to_know(message: types.Message, state: FSMContext):
    """
    process subjects to know
    """
    async with state.proxy() as data:

        data['subjects_to_learn'] = message.text
        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

            # And send message
        await bot.send_message(
           message.chat.id,
           md.text(
              md.text('Твой никнейм: ', md.bold(data['nickname'])),
              md.text('Год обучения: ', data['school_grade']),
              md.text('Предметы в которых ты шаришь: ', data['subjects_user_know']),
              md.text('Предметы в которых ты хочешь шарить: ', data['subjects_to_learn']),
              sep='\n',
           ),
           reply_markup=markup,
           parse_mode=ParseMode.MARKDOWN,
        )

        user_registration_datetime = str(datetime.datetime.now())
        #for sending it to a db_handler
        some_user = User(
           user_registration_datetime,
           data['nickname'],
           data['school_grade'],
           data['subjects_user_know'],
           data['subjects_to_learn'],
        )

        some_user.save_to_db()


    # Finish conversation
    await state.finish()
