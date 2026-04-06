from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class NewsItemBase(BaseModel):
    id: int = Field(description="新闻ID")
    title: str = Field(description="新闻标题")
    description: Optional[str] = Field(None, description="新闻简介")
    image: Optional[str] = Field(None, description="新闻图片")
    author: Optional[str] = Field(None, description="新闻作者")
    category_id: int = Field(alias="categoryId", description="分类ID")
    views: int = Field(description="浏览量")
    publish_time: Optional[datetime] = Field(None, description="发布时间")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )