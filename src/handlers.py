from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session

import datetime

from states import CalenderSetting
from db import engine, User, Task
from keyboards import main_keyboard

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            user = User(id=user_id)
            session.add(user)
            session.commit()
    await message.answer("Choose option:", reply_markup=main_keyboard)


########## Set Notification Time ##########

@router.message(lambda message: message.text == "Set Notification Time")
async def command_set_notification_time_handler(message: Message, state: FSMContext) -> None:
    await message.answer("What time is best for you? Please provide the time in HH:MM format:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CalenderSetting.setting_notification_time)

@router.message(CalenderSetting.setting_notification_time)
async def process_notification_time(message: Message, state: FSMContext) -> None:
    try:
        notification_time = datetime.datetime.strptime(message.text, "%H:%M").time()
        user_id = message.from_user.id

        with Session(engine) as session:
            user = session.get(User, user_id)
            if user:
                user.notification_time = notification_time
                session.commit()
                await message.answer(f"Notification time set to {notification_time}.")
            else:
                await message.answer("User not found.")

        await state.clear()
        await message.answer("Choose option:", reply_markup=main_keyboard)

    except ValueError:
        await message.answer("Invalid time format. Please use HH:MM format.")

########## Add Task ##########

@router.message(lambda message: message.text == 'Add Task')
async def command_add_task_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"When do you need to do this task? Please provide the time in format MM.YYYY.DD HH:MM: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CalenderSetting.adding_task_time)

@router.message(CalenderSetting.adding_task_time)
async def process_adding_task(message: Message, state: FSMContext) -> None:
    try:
        task_time = datetime.datetime.strptime(message.text, "%m.%Y.%d %H:%M")
        await state.update_data(task_time=task_time)

        await message.answer("Task time recorded. Please provide the notification time in format MM.YYYY.DD HH:MM:")
        await state.set_state(CalenderSetting.adding_task_notification_time)

    except ValueError:
        await message.answer('Invalid time format. Please use MM.YYYY.DD HH:MM format.')

@router.message(CalenderSetting.adding_task_notification_time)
async def process_adding_task_notification_time(message: Message, state: FSMContext) -> None:
    try:
        task_notification_time = datetime.datetime.strptime(message.text, "%m.%Y.%d %H:%M")
        await state.update_data(task_notification_time=task_notification_time)

        await message.answer("Notification time recorded. Please provide the text of the task:")
        await state.set_state(CalenderSetting.adding_task_text)
    except ValueError:
        await message.answer('Invalid time format. Please use MM.YYYY.DD HH:MM format.')

@router.message(CalenderSetting.adding_task_text)
async def process_adding_task_text(message: Message, state: FSMContext) -> None:
    task_text = message.text
    user_id = message.from_user.id

    state_data = await state.get_data()
    task_time = state_data.get("task_time")
    task_notification_time = state_data.get("task_notification_time")

    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            task = Task(
                text=task_text,
                timestamp=task_time,
                notification_datetime=task_notification_time,
                user=user
            )

            session.add(task)
            session.commit()
            await message.answer("Task successfully added.", reply_markup=main_keyboard)
        else:
            await message.answer("User not found. Please start the bot with /start.")

        await state.clear()

########## Show All Tasks ##########

@router.message(lambda message: message.text == 'Show All Tasks')
async def command_show_all_tasks_handler(message: Message) -> None:
    user_id = message.from_user.id

    with Session(engine) as session:
        tasks = session.query(Task).filter_by(user_id=user_id).all()

        if tasks:
            response = '\n'.join(f'TIMESTAMP: {task.timestamp} TEXT: {task.text}' for task in tasks)
        else:
            response = "No tasks"

    await message.answer(response)