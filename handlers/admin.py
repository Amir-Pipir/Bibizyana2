import asyncio
import os
import pydoc

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.enums import ParseMode
from datetime import datetime
from aiogram.filters.callback_data import CallbackData
import re
from database.orm_query import *
from kbd import *
from middlewares.filter import IsAdmin
from create_bot import bot

admin_router = Router()
admin_router.message.filter(IsAdmin())


class Spam(StatesGroup):
    text = State()


@admin_router.message(Command("get"))
async def get_user_len(mes: Message, session: AsyncSession):
    users = await orm_get_all_users(session)
    await mes.answer(f"Всего польззователей: {len(users)}")


@admin_router.message(Command("get_db"))
async def send_db(mes: Message):
    file = FSInputFile("bot.db")
    await bot.send_document(chat_id=mes.from_user.id, document=file)


@admin_router.message(Command("message"))
async def messages(mes: Message, state: FSMContext):
    await mes.answer("Отправьте послание бибизянам")
    await state.set_state(Spam.text)


@admin_router.message(Spam.text)
async def content(mes: Message, state: FSMContext, session: AsyncSession):
    await mes.answer("Ваше сообщение отправляется, ждите")
    users = await orm_get_all_users(session)
    for user in users:
        try:
            if mes.text:
                await bot.send_message(chat_id=user.tg_id, text=mes.text)
            if mes.photo:
                await bot.send_photo(chat_id=user.tg_id, photo=mes.photo[-1].file_id, caption=mes.caption)
            if mes.video:
                await bot.send_video(chat_id=user.tg_id, video=mes.video.file_id, caption=mes.caption)
            if mes.animation:
                await bot.send_animation(chat_id=user.tg_id, animation=mes.animation.file_id, caption=mes.caption)
        except:
            await orm_delete_user(session, user.tg_id)
    await mes.answer("Ваше сообщение было успешно доставлено всем пользователям")
    await state.clear()





