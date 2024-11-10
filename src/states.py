from aiogram.fsm.state import StatesGroup, State

class CalenderSetting(StatesGroup):
	setting_notification_time = State()

	adding_task_time = State()
	adding_task_notification_time = State()
	adding_task_text = State()