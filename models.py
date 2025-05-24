from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    is_done: Mapped[bool] = mapped_column(server_default='false')

    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.NOW())
    updated_at: Mapped[datetime] = mapped_column(server_default=sa.func.NOW(), onupdate=sa.func.NOW())
