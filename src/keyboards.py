from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Set Notification Time"), KeyboardButton(text="Add Task")],
            [KeyboardButton(text="Set Task Notification Time"), KeyboardButton(text="Show All Tasks")]
        ],
        resize_keyboard=True
    )