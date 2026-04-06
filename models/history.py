
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass



class History(Base):
    __tablename__ = "history"

    #创建索引
    __table_args__ = (
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
        Index("idx_view_time", "view_time")
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史记录ID")
    user_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="新闻ID"
    )
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, server_default=func.now(), comment="浏览时间")

    def __repr__(self) -> str:
        return f"History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})"