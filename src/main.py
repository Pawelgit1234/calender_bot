import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from handlers import router
from schedulers import scheduled_task_notification, scheduled_weather_notification

load_dotenv()

TOKEN = getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKEN)

async def main() -> None:
	dp.include_router(router)

	polling_task = dp.start_polling(bot)
	scheduler_task = scheduled_task_notification(bot)
	scheduler_user = scheduled_weather_notification(bot)

	await asyncio.gather(polling_task, scheduler_task, scheduler_user)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass