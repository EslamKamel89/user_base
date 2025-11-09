from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class User(Base , TimestampMixin) :
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(String(120) , nullable=False)
    email:Mapped[str] = mapped_column(String(255), nullable=False , index=True , unique=True)
    password_hash:Mapped[str] = mapped_column(String(255), nullable=False )