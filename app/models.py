from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import func

class Model(DeclarativeBase):
   pass

class Projects(Model):
   __tablename__ = "projects"
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str]
   location: Mapped[str]
   status: Mapped[str]
   created_at: Mapped[datetime] = mapped_column(default=func.now())

class Tasks(Model):
   __tablename__ = "tasks"
   id: Mapped[int] = mapped_column(primary_key=True)
   project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
   name: Mapped[str]
   status: Mapped[str]