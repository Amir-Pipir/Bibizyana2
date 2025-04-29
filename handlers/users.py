import pprint

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.enums import ParseMode
from datetime import datetime
from aiogram.filters.callback_data import CallbackData
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re
from database.orm_query import *
from kbd import *
from create_bot import bot

import datetime as dt
from monkey import monkey

import random

user_router = Router()

main_kb = reply_kb(btns=[['Какой я бибизян сиводня']])


@user_router.message(F.text.lower() == "отмена", F.chat.type == "private")
@user_router.message(Command("stop"), F.chat.type == "private")
async def state_cansel(mes: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state:
        await state.clear()
    await mes.answer("Действие отменено")


@user_router.message(CommandStart())
async def start(mes: Message, session: AsyncSession):
    user = await orm_get_user(session, mes.from_user.id)

    if user is None:
        await orm_add_user(session, mes.from_user.id)
        text = "Пливеть, тилиглам бибизян. Тут ти мозиш виблать какой ти бибизян сиводня. Зми кнапку «Какой я бибизян» и каздий день будис знат своиво бибизян"
        await mes.answer(text, reply_markup=reply_kb(btns=[['Какой я бибизян']]))
        return

    await mes.answer("Ты скоро узнаешь какой ты бибизян, жди!", reply_markup=main_kb)


@user_router.message(F.text == 'Какой я бибизян')
async def get_monkey(message: Message, session: AsyncSession):
    now = dt.datetime.now()
    if now.hour > 12:
        await message.answer("Типерь ти бибизян. Каздий день ти будис знат своиво бибизяна!")
        random_monkey = random.choice(monkey)
        await message.answer_sticker(random_monkey["sticker_id"])
        await message.answer(random_monkey["text"], reply_markup=main_kb)

    elif now.hour < 12:
        await message.answer("Типерь ти бибизян. Каздий день ти будис знат своиво бибизяна!")
        await message.answer('Зди сваего бибизяна сиводня или нажми кнапку Какой я бибизян', reply_markup=main_kb)


@user_router.message(F.text == 'Какой я бибизян сиводня')
async def get_monkey_today(mes: Message, session: AsyncSession):
    user = await orm_get_user(session, mes.from_user.id)
    if user.monkey_status == 1:
        random_monkey = random.choice(monkey)
        await mes.answer_sticker(random_monkey["sticker_id"])
        await mes.answer(random_monkey["text"], reply_markup=main_kb)
        await orm_update_status(session, mes.from_user.id, False)
    else:
        await mes.answer('На сиводня фсёёё! Зди сваего бибизяна', reply_markup=main_kb)
