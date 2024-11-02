from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Set Time"), KeyboardButton(text="Add Task")],
            [KeyboardButton(text="Set Notification Time"), KeyboardButton(text="Show All Tasks")]
        ],
        resize_keyboard=True
    )
    await message.answer("Choose option:", reply_markup=keyboard)

@router.message(Command('settime'))
async def command_set_time_handler(message: Message) -> None: #sends at time information
    await message.answer(f"Time set")

@router.message(Command('addtask'))
async def command_add_task_handler(message: Message) -> None:
    await message.answer(f"Time set")

@router.message(Command('settasknotificationtime'))
async def command_set_notification_time_handler(message: Message) -> None:
    await message.answer(f"Time set")

@router.message(Command('showalltasks'))
async def command_show_all_tasks_handler(message: Message) -> None:
    await message.answer(f"Time set")