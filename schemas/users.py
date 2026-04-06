from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.fields import Field



class UserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像")
    gender: Optional[str] = Field(None, description="性别")
    bio: str = Field(..., description="个人简介")
    phone: Optional[str] = Field(None, description="手机号")


class UserInfoResponse(UserInfoBase):
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


# data 数据类型
class UserAuthResponse(BaseModel):
    token: str = Field(..., description="Token")
    user_info: UserInfoResponse = Field(..., alias="userInfo", description="用户信息")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )



# 更新用户信息请求体
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像")
    gender: Optional[str] = Field(None, description="性别")
    bio: Optional[str] = Field(None, description="个人简介")
    phone: Optional[str] = Field(None, description="手机号")
    


class UserPasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=20, alias="newPassword", description="新密码")
