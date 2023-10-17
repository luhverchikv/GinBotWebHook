import asyncio
import datetime
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from simple_calendar.Simple_Calendar import SimpleCalendar, SimpleCalendarCallback as simple_cal_callback
from loguru import logger

calendar_router = Router()


async def delete_message(message: Message, seconds: int = 0):
    await asyncio.sleep(seconds)
    await message.delete(reply_markup=None)


@calendar_router.message(F.text == 'Сегодня')
async def process_today(message: Message) -> None:
    now = datetime.datetime.now()
    future = now + datetime.timedelta(days=125)  # на один день меньше, так как счет не с 0, а с 1.
    future_date = future.strftime('%d.%m.%Y')
    answer = await message.answer(f"Сегодня: {now.strftime('%d.%m.%Y')}\nЧерез 126 дней: {future_date}")
    logger.info(f'Пользователь {message.from_user.id} нажал Сегодня')
    asyncio.create_task(delete_message(message, 1))
    asyncio.create_task(delete_message(answer, 10))


@calendar_router.message(F.text == 'Календарь')
async def process_calendar(message: Message) -> None:
    await message.answer("Выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())
    logger.info(f'Пользователь {message.from_user.id} нажал Календарь')
    asyncio.create_task(delete_message(message, 5))


# simple calendar usage
@calendar_router.callback_query(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        future = date + datetime.timedelta(days=125)
        today = datetime.datetime.now()
        ultrasound_1 = (f'{(date + datetime.timedelta(days=76)).strftime("%d.%m.%Y")} - '
                        f'{(date + datetime.timedelta(days=96)).strftime("%d.%m.%Y")}')  # 11 недель -13 недель + 6 дней
        ultrasound_2 = (f'{(date + datetime.timedelta(days=139)).strftime("%d.%m.%Y")} - '
                        f'{(date + datetime.timedelta(days=153)).strftime("%d.%m.%Y")}')  # 20 - 22 недели
        ultrasound_3 = (f'{(date + datetime.timedelta(days=223)).strftime("%d.%m.%Y")} - '
                        f'{(date + datetime.timedelta(days=237)).strftime("%d.%m.%Y")}')  # 32 - 34 недели
        answer = await callback_query.message.answer(f'Вы выбрали: {date.strftime("%d.%m.%Y")}\n'
                                                     f'Через 126 дней: {future.strftime("%d.%m.%Y")}'
                                                     f'\n_______________________\n\n\n'
                                                     f'<b>Первый день последних месячных:</b> '
                                                     f'{date.strftime("%d.%m.%Y")}\n\n'
                                                     f'<b>Сегодня:</b> {today.strftime("%d.%m.%Y")}, '
                                                     f'это {(today - date).days // 7} недель '
                                                     f'или {(today - date).days} дней\n\n'
                                                     f'<b>УЗИ №1:</b> {ultrasound_1}\n\n'
                                                     f'<b>УЗИ №2:</b> {ultrasound_2}\n\n'
                                                     f'<b>УЗИ №3:</b> {ultrasound_3}\n\n'
                                                     f'<b>30 недель:</b> '
                                                     f'{(date + datetime.timedelta(days=209)).strftime("%d.%m.%Y")}\n\n'
                                                     f'<b>Предполагаемые даты ЛН:</b> '
                                                     f'{(date + datetime.timedelta(days=209)).strftime("%d.%m.%Y")}-'
                                                     f'{(date + datetime.timedelta(days=334)).strftime("%d.%m.%Y")}\n\n'
                                                     f'<b>Предполагаемая дата родов:</b> '
                                                     f'{(date + datetime.timedelta(days=279)).strftime("%d.%m.%Y")}')
        asyncio.create_task(delete_message(callback_query.message, 5))
        asyncio.create_task(delete_message(answer, 100))
