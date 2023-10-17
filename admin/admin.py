from keyboard.keyboard import start_kb
from aiogram import F, Router
from aiogram.types import Message
from loguru import logger

admin_router = Router()


@admin_router.message(F.text == 'О Ферретаб')
async def process_ferretab(message: Message):
    await message.answer('Ferretab.by - это сайт, посвященный проблеме анемий и дефицита железа. '
                         'Вы можете посетить сайт Ferretab.by, перейдя по ссылке: https://ferretab.by',
                         reply_markup=start_kb)
    logger.info(f'Пользователь {message.from_user.id} нажал О Ферретаб')
