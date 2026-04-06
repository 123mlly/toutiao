from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


"""
检查是否收藏
"""
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    # 是否有收藏记录
    return result.scalar_one_or_none() is not None


"""
添加收藏
"""
async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

"""
取消收藏
"""
async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# 获取用户的收藏列表
async def get_favorite_list(db: AsyncSession, user_id: int, page: int, page_size: int = 10):

        # 总量 + 收藏列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()


    # 获取收藏列表 - 联表查询 join() + 分页
    news_query = (select(News,Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
                .join(Favorite,Favorite.news_id == News.id)
                .where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())
                .offset((page - 1) * page_size).limit(page_size)
                )
    
    news_result = await db.execute(news_query)
    news_list = news_result.all()
    return news_list, total


"""
清空所有收藏列表
"""
async def remove_all_favorite(db: AsyncSession, user_id: int):
    delete_query = delete(Favorite).where(Favorite.user_id == user_id)
    result  = await db.execute(delete_query)
    await db.commit()
    return result.rowcount or 0




