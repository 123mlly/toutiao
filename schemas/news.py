from pydantic import BaseModel, Field


class CategoryListData(BaseModel):
    """新闻列表 / 分类列表等业务数据体：分页元信息 + 列表."""

    total: int = Field(0, description="总条数")
    skip: int = Field(0, description="跳过条数")
    page_size: int = Field(10, description="本页条数")
    categories: list[dict] = Field(default_factory=list, description="分类列表")


class CategoryListResponse(BaseModel):
    """统一接口外壳：业务码 + 提示 + data."""

    code: int = Field(200, description="业务状态码，成功为 200")
    message: str = Field(..., description="提示信息")
    data: CategoryListData
