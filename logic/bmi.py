import asyncio
from keyboard.keyboard import start_kb
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from loguru import logger


bmi_router = Router()


async def delete_message(message: Message, seconds: int = 0):
    await asyncio.sleep(seconds)
    await message.delete(reply_markup=None)


class BMI(StatesGroup):
    weight = State()
    height = State()


@bmi_router.message(F.text == 'ИМТ')
async def process_bmi(message: Message, state: FSMContext) -> None:
    await state.set_state(BMI.weight)
    answer = await message.answer('Введите вес в кг:')
    asyncio.create_task(delete_message(message, 1))
    asyncio.create_task(delete_message(answer, 30))


@bmi_router.message(BMI.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    weight = message.text
    if "," in weight:
        new_weight = weight.replace(",", ".")
    else:
        new_weight = weight
    if new_weight.isdigit():
        if 40 <= float(new_weight) <= 240:
            await state.update_data(weight=float(new_weight))
            await state.set_state(BMI.height)
            answer = await message.answer("Введите рост в см:")
            asyncio.create_task(delete_message(message, 1))
            asyncio.create_task(delete_message(answer, 30))
    elif new_weight.isalpha():
        nb_answer = await message.answer("Пожалуйста, введите вес в диапазоне от 40 до 160 кг.")
        asyncio.create_task(delete_message(nb_answer, 30))
    elif bool(float(new_weight)):
        if 40 <= float(new_weight) <= 160:
            await state.update_data(weight=float(new_weight))
            await state.set_state(BMI.height)
            answer = await message.answer("Введите рост в см:")
            asyncio.create_task(delete_message(message, 1))
            asyncio.create_task(delete_message(answer, 30))
    else:
        nb_answer = await message.answer("Пожалуйста, введите вес в диапазоне от 40 до 160 кг.")
        asyncio.create_task(delete_message(nb_answer, 30))


@bmi_router.message(BMI.height)
async def process_height(message: Message, state: FSMContext) -> None:
    height = int(message.text)
    if 120 <= height <= 220:
        data = await state.update_data(height=float(message.text))
        await state.clear()
        await get_bmi(message=message, data=data)
        asyncio.create_task(delete_message(message, 1))
    else:
        answer = await message.answer("Пожалуйста, введите рост в диапазоне от 120 до 220 см.")
        asyncio.create_task(delete_message(answer, 5))


async def get_bmi(message: Message, data) -> None:
    weight = float(data["weight"])
    height = data["height"] / 100
    bmi = weight / (height ** 2)
    if bmi >= 25.0:
        ideal_weight = 24.99 * (height ** 2)
        obisety = weight - ideal_weight
        text_send = f'\nИзбыточный вес {round(obisety, 1)} кг!'
    else:
        text_send = ''
    await message.answer(f'Вес: {weight} кг\nРост: {height} м\nИМТ = {round(bmi, 1)}' + text_send,
                         reply_markup=start_kb)
    logger.info(f'Пользователь {message.from_user.id} вычислил ИМТ={round(bmi, 1)}')
