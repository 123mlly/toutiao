from datetime import datetime
from typing import Optional
from sqlalchemy import Enum as SAEnum, UniqueConstraint
from sqlalchemy import Index, DateTime, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func




class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, server_default=func.now(), comment="更新时间")


class BaseEmpty(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        UniqueConstraint("username", name="username_UNIQUE"),   
        UniqueConstraint("phone", name="phone_UNIQUE"),
    )


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(20), nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希")
    nickname: Mapped[Optional[str]] = mapped_column(String(20), comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment="头像")
    gender: Mapped[Optional[str]] = mapped_column(
        SAEnum(
            "male",
            "female",
            "unknown",
            name="user_gender_enum",
            native_enum=True,
            validate_strings=True,
        ),
        default="unknown",
        server_default=text("'unknown'"),
        comment="性别（与 MySQL ENUM 一致）",
    )
    bio: Mapped[str] = mapped_column(String(255), default="这个人很懒，什么都没留下", comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String(11), comment="手机号")


    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, password={self.password}, nickname={self.nickname}, avatar={self.avatar}, gender={self.gender}, bio={self.bio}, phone={self.phone})"



class UserToken(BaseEmpty):
    __tablename__ = "user_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment="Token")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, server_default=func.now(), comment="创建时间")

    def __repr__(self) -> str:
        return f"UserToken(id={self.id}, user_id={self.user_id}, token={self.token}, created_at={self.created_at}, updated_at={self.updated_at})"
