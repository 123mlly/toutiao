

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from models.news import News

# 添加历史记录
async def add_news_history(db: AsyncSession, user_id: int, news_id: int):
    # 检查是否存在历史记录
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    if history:
        return history

    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


# 获取历史记录列表
async def get_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    # 总量
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 获取历史记录列表
    offset = (page - 1) * page_size
    query = (select(News, History.id.label("history_id"), History.view_time.label("view_time"))
            .join(History, History.news_id == News.id)
            .where(History.user_id == user_id)
            .order_by(History.view_time.desc())
            .offset(offset)
            .limit(page_size))
    result = await db.execute(query)
    rows = result.all()
    
    return rows, total


# 删除单条历史记录
async def remove_item_history(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0


async def remove_all_history(db: AsyncSession, user_id: int):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0