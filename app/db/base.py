from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TimestampMixin :
    created_at:Mapped[datetime | None] = mapped_column(DateTime(timezone=True) , server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True) , onupdate=func.now() , nullable=True)
class Base(DeclarativeBase) :
    pass