import asyncio
from datetime import datetime

from sqlalchemy.orm import Session

from db import Task, engine, User
from api import get_weather

async def scheduled_task_notification(bot) -> None:
	""" Sends notifications about tasks to users and delete them after it """
	while True:
		now = datetime.now()

		with Session(engine) as session:
			tasks = session.query(Task).filter(Task.notification_datetime <= now).all()

			for task in tasks:
				await bot.send_message(task.user_id, f"You have a task at {task.timestamp}: {task.text}")
				session.delete(task)
				session.commit()

		await asyncio.sleep(10) # check every 10 seconds if there are tasks to notify

async def scheduled_weather_notification(bot) -> None:
	""" Sends to user the weather notification """
	last_reset_date = datetime.now().date()

	while True:
		now = datetime.now()

		if now.date() != last_reset_date:
			with Session(engine) as session:
				session.query(User).update({User.was_notified: False})
				session.commit()
			last_reset_date = now.date()

		with Session(engine) as session:
			users = session.query(User).filter((User.notification_time < now) & (User.was_notified == False)).all()

			for user in users:
				weather = await get_weather(user.lat, user.lon)
				await bot.send_message(user.id, f"Today will be: {weather}")
				user.was_notified = True
				session.commit()

		await asyncio.sleep(10)