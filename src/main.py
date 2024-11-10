import asyncio
import logging
import sys
from datetime import datetime
from os import getenv

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from sqlalchemy.orm import Session

from handlers import router
from db import Task, engine

load_dotenv()

TOKEN = getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKEN)

async def scheduled_task():
	while True:
		now = datetime.now()

		with Session(engine) as session:
			tasks = session.query(Task).filter(Task.notification_datetime <= now).all()

			for task in tasks:
				await bot.send_message(task.user_id, f"You have a task at {task.timestamp}: {task.text}")
				session.delete(task)
				session.commit()

		await asyncio.sleep(10) # check every 10 seconds if there are tasks to notify

async def main() -> None:
	dp.include_router(router)

	polling_task = dp.start_polling(bot)
	scheduler_task = scheduled_task()

	await asyncio.gather(polling_task, scheduler_task)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass