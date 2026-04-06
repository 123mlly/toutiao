from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from schemas.news import CategoryListData, CategoryListResponse
from crud import news
from utils.response import ok

router = APIRouter(prefix="/api/news", tags=["新闻"])


@router.get(
    "/categories",
    # response_model=CategoryListResponse,
    summary="新闻分类列表",
)
async def get_categories(
    skip: int = Query(0, ge=0, description="跳过条数"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
    db: AsyncSession = Depends(get_db),
):
    categories = await news.get_categories(db, skip, page_size)

    return ok(
        message="获取分类成功",
        data=categories,
    )

@router.get(
    "/list",
    summary="新闻列表"
)
async def get_news_list(
    category_id: int = Query(..., ge=0, alias="categoryId",description="分类ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize", description="每页条数"),
    db: AsyncSession = Depends(get_db),
):
    # 先处理分页规则 -> 查询新闻列表 -> 计算总量 --> 计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_list)) < total

    return ok(
        message="获取新闻列表成功",
        data={"list": news_list, "total": total, "hasMore": has_more},
    )



@router.get(
    "/detail",
    summary="新闻详情"
)
async def get_news_detail(
    news_id: int = Query(..., ge=0, alias="id",description="新闻ID"),
    db: AsyncSession = Depends(get_db),
):
    news_detail = await news.get_news_detail(db, news_id)
    if news_detail is None:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    vies_res =  await news.update_news_views(db, news_id)

    if not vies_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    related_news = await news.get_related_news(db, news_id, news_detail.category_id)

    return ok(
        message="获取新闻详情成功",
        data= {
            **jsonable_encoder(news_detail),
            "relatedNews": [jsonable_encoder(item) for item in related_news]
        },
    )
