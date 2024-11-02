import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from handlers import router

load_dotenv()

TOKEN = getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKEN)

async def main() -> None:
	dp.include_router(router)
	await dp.start_polling(bot)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass