from unittest import async_case
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from cache.news_cache import get_categories_cache, set_categories_cache
from models.news import Category, News

"""
获取新闻分类列表
"""
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    cached_categories = await get_categories_cache()
    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    if categories:
        await set_categories_cache(jsonable_encoder(categories), 7200)
    
    return categories


"""
获取新闻列表
"""
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, linmit: int = 10):
    
    # 查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(linmit)
    result = await db.execute(stmt)
    return result.scalars().all()


"""
获取新闻总数
"""
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


"""
获取新闻详情
"""
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


"""
更新新闻浏览量
"""
async def update_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount > 0


""""
获取相关新闻
"""
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    stmt = select(News).where(News.category_id == category_id , News.id != news_id).order_by(News.views.desc(), News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()