from aiogram.fsm.state import StatesGroup, State

class CalenderSetting(StatesGroup):
	setting_notification_time = State()
	adding_task = State()
	setting_task_notification_time = State()