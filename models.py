from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class UsersModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    status: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    role:Mapped[str] = mapped_column()


class PostsModel(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_topic: Mapped[str] = mapped_column()
    post_name: Mapped[str] = mapped_column()
    post_body: Mapped[str] = mapped_column()
    #user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))