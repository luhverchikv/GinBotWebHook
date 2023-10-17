import asyncio
from aiogram import F, Router
from keyboard.keyboard import start_kb, sex_kb, kreat_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from loguru import logger


gfr_router = Router()


async def delete_message(message: Message, seconds: int = 0):
    await asyncio.sleep(seconds)
    await message.delete(reply_markup=None)


class GFR(StatesGroup):
    sex = State()
    age = State()
    kreat = State()
    gfr = State()


@gfr_router.message(F.text == 'СКФ')
async def process_bmi(message: Message, state: FSMContext):
    await state.set_state(GFR.sex)
    answer = await message.answer('Укажите пол:', reply_markup=sex_kb)
    asyncio.create_task(delete_message(message, 1))
    asyncio.create_task(delete_message(answer, 10))


@gfr_router.message(GFR.sex)
async def process_sex_man(message: Message, state: FSMContext) -> None:
    await state.update_data(sex=message.text)
    await state.set_state(GFR.age)
    answer = await message.answer('Укажите возраст:')
    asyncio.create_task(delete_message(message, 1))
    asyncio.create_task(delete_message(answer, 10))


@gfr_router.message(GFR.age)
async def process_age(message: Message, state: FSMContext) -> None:
    age = int(message.text)
    if 18 <= age <= 99:
        await state.update_data(age=int(message.text))
        await state.set_state(GFR.kreat)
        answer = await message.answer('Укажите единицы измерения креатинина:',
                                      reply_markup=kreat_kb)
        asyncio.create_task(delete_message(message, 1))
        asyncio.create_task(delete_message(answer, 10))
    else:
        age_answer = await message.answer('Укажите возраст от 18 до 99')
        asyncio.create_task(delete_message(age_answer, 10))


@gfr_router.message(GFR.kreat)
async def process_gfr(message: Message, state: FSMContext) -> None:
    await state.update_data(kreat=message.text)
    await state.set_state(GFR.gfr)
    answer = await message.answer('Укажите уровень креатинина:')
    asyncio.create_task(delete_message(message, 1))
    asyncio.create_task(delete_message(answer, 10))


@gfr_router.message(GFR.gfr)
async def process_gfr(message: Message, state: FSMContext) -> None:
    data_gfr = await state.update_data(gfr=float(message.text))
    await state.clear()
    await get_gfr(message=message, data=data_gfr)
    asyncio.create_task(delete_message(message, 1))


async def get_gfr(message: Message, data):
    age = data['age']
    if data['kreat'] == 'мкмоль/л':
        scr = data['gfr'] * 0.0113
    else:
        scr = data['gfr']
    if data['sex'] == 'Мужской':
        k = 0.9
        alpha = -3.02
        s = 1
    else:
        k = 0.7
        alpha = -0.241
        s = 1.012
    result = 142 * (min(scr/k, 1) ** alpha) * (max(scr/k, 1)**(-1.200)) * (0.9938 ** age) * s

    await message.answer(f'{round(result, 1)} мл/мин/1,73 м²',
                         reply_markup=start_kb)
    logger.info(f'Пользователь {message.from_user.id} вычислил СКФ={round(result, 1)}')
