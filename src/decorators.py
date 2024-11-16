from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.orm import Session

from db import engine, User


def check_registration(func):
	async def wrapper(message: Message, state: FSMContext) -> None:
		with Session(engine) as session:
			user = session.query(User).filter_by(id=message.from_user.id).first()
			if user is None:
				await message.answer("Please log in with /start.")
			else:
				await func(message, state)
	return wrapper

