from sqlalchemy import DateTime, String, Time, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from datetime import time, datetime


class Base(DeclarativeBase):
	pass

class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True) # Telegram ID
	notification_time: Mapped[time] = mapped_column(Time, default=time(6, 0))
	tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")

class Task(Base):
	__tablename__ = 'tasks'

	id: Mapped[int] = mapped_column(primary_key=True)
	text: Mapped[str] = mapped_column(String(300))
	timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)
	notification_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	user: Mapped["User"] = relationship("User", back_populates="tasks")

engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)