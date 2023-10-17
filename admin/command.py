import logging
from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, ReplyKeyboardRemove)
from aiogram.methods.send_message import SendMessage
from keyboard.keyboard import start_kb
from loguru import logger
from admin.db import Database


db = Database('admin/database.db')


command_router = Router()


@command_router.message(CommandStart())
async def command_start(message: Message, bot: Bot) -> None:
    if db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           "Добро пожаловать!",
                           reply_markup=start_kb)
    logger.info(f'Пользователь {message.from_user.id} присоеденился!')


@command_router.message(Command("cancel"))
@command_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@command_router.message(Command("sendall"))
async def sendall(message: Message, bot: Bot) -> None:
    if message.chat.type == 'private' and message.from_user.id == 40213208:
        text = message.text[9:]
        users = db.get_users()
        for row in users:
            try:
                await bot(SendMessage(chat_id=row[0], text=text))  # bot.send_message(row[0], text)
                if int(row[1]) == 0:
                    db.set_active(row[0], 1)
            except:
                db.set_active(row[0], 0)
        await message.reply('Успешно разослано!')
