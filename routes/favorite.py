from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.favorite import add_news_favorite, get_favorite_list, is_news_favorite, remove_all_favorite, remove_news_favorite
from models.users import User
from schemas.base import NewsItemBase
from schemas.favorite import (
    FavoriteListResponse,
    FavoriteNewsItemResponse,
    FavoriteRequest,
    FavoriteResponse,
)
from utils.response import ok
from utils.auth import get_current_user


router = APIRouter(prefix="/api/favorite", tags=["收藏"])


@router.get("/check", summary="检查是否收藏")
async def check_favorite(
    news_id: int = Query(..., ge=0, alias="newsId",description="新闻ID"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    is_favorite = await is_news_favorite(db, user.id, news_id)
    return ok(message="检查是否收藏成功", data=FavoriteResponse(isFavorite=is_favorite))


@router.post("/add", summary="添加收藏")
async def add_favorite(
    data: FavoriteRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    
    favorite = await add_news_favorite(db, user.id, data.news_id)
    
    return ok(message="添加收藏成功", data=favorite)


@router.delete("/remove", summary="取消收藏")
async def remove_favorite(
    news_id: int = Query(..., ge=0, alias="newsId",description="新闻ID"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    is_removed_favorite = await remove_news_favorite(db, user.id, news_id) 

    if not is_removed_favorite:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="取消收藏失败")
        
    return ok(message="取消收藏成功")



@router.get("/list", summary="获取收藏列表")
async def query_favorite_list(
    page: int = Query(1, ge=1 ,description="页码"),
    page_size: int = Query(10, ge=1, alias="pageSize",description="每页条数"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows, total = await get_favorite_list(db, user.id, page, page_size)

    items: list[FavoriteNewsItemResponse] = [
        FavoriteNewsItemResponse(
            **NewsItemBase.model_validate(news).model_dump(),
            favorite_id=favorite_id,
            favorite_time=favorite_time,
        )
        for news, favorite_time, favorite_id in rows
    ]
    offset = (page - 1) * page_size
    has_more = offset + len(items) < total

    return ok(
        message="获取收藏列表成功",
        data=FavoriteListResponse(total=total, items=items, has_more=has_more),
    )



@router.delete("/clear", summary="取消所有收藏")
async def clear_favorite(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    removed_count = await remove_all_favorite(db, user.id)
    return ok(message=f"取消所有收藏成功，共取消 {removed_count} 条收藏", data=removed_count)



