from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from schemas.base import NewsItemBase

class HistoryRequest(BaseModel):
    news_id: int = Field(..., ge=0, alias="newsId",description="新闻ID")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

  
class HistoryItemResponse(NewsItemBase):
    history_id: int = Field(alias="historyId", description="历史记录ID")
    view_time: datetime = Field(alias="viewTime", description="历史记录时间")

    @field_serializer("view_time")
    def _fmt_history_time(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")

class HistoryListResponse(BaseModel):
    total: int = Field(description="总条数")
    items: list[HistoryItemResponse] = Field(alias="list",description="历史记录列表")
    has_more: bool = Field(alias="hasMore", description="是否有更多")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )