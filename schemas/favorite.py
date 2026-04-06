from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from schemas.base import NewsItemBase


class FavoriteResponse(BaseModel):
    is_favorite: bool = Field(..., description="是否收藏", alias="isFavorite")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
    
class FavoriteRequest(BaseModel):
    news_id: int = Field(..., ge=0, alias="newsId",description="新闻ID")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(..., alias="favoriteId", description="收藏ID")
    favorite_time: datetime = Field(..., alias="favoriteTime", description="收藏时间")
    
    @field_serializer("favorite_time")
    def _fmt_favorite_time(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")
    
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


# 收藏列表模型类
class FavoriteListResponse(BaseModel):
    total: int = Field(..., description="总条数")
    items: list[FavoriteNewsItemResponse] = Field(
        ...,
        alias="list",
        description="收藏列表",
    )
    has_more: bool = Field(..., alias="hasMore", description="是否有更多")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )




