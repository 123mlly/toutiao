from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.history import add_news_history, get_history_list, remove_all_history, remove_item_history
from models.users import User
from schemas.base import NewsItemBase
from schemas.history import HistoryItemResponse, HistoryListResponse, HistoryRequest
from utils.auth import get_current_user
from utils.response import ok


router = APIRouter(prefix="/api/history", tags=["历史记录"])


@router.post("/add", summary="添加历史记录")
async def add_history(
    data: HistoryRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):  
    history = await add_news_history(db, user.id, data.news_id)

    return ok(message="添加历史记录成功", data=history)


@router.get("/list", summary="获取历史记录列表")
async def query_history_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, alias="pageSize",description="每页条数"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    history_list, total = await get_history_list(db, user.id, page, page_size)

    items: list[HistoryItemResponse] = [
        HistoryItemResponse(
            **NewsItemBase.model_validate(news).model_dump(),
            history_id=history_id,
            view_time=view_time,
        )
        for news, history_id, view_time in history_list
    ]

    has_more = (page - 1) * page_size + len(items) < total

    return ok(message="获取历史记录列表成功", data=HistoryListResponse(total=total, items=items, has_more=has_more))


# 清除单条历史记录
@router.delete("/delete/{news_id}", summary="清除单条历史记录")
async def delete_item_history(
    news_id: int = Path(..., ge=0, description="历史记录ID"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    deleted_count = await remove_item_history(db, user.id, news_id)
    return ok(message=f"清除单条历史记录成功，共清除 {deleted_count} 条历史记录", data=deleted_count)


# 清空历史记录
@router.delete("/clear", summary="清空历史记录")
async def clear_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    deleted_count = await remove_all_history(db, user.id)
    return ok(message=f"清空历史记录成功，共清除 {deleted_count} 条历史记录", data=deleted_count)