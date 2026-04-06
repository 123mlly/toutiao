from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import authenticate_user, create_user, generate_token, get_user_by_username, update_user_info, update_user_password
from models.users import User
from schemas.users import UserAuthResponse, UserInfoResponse, UserPasswordRequest, UserRequest, UserUpdateRequest
from utils.auth import get_current_user
from utils.response import fail, ok

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.post("/register", summary="注册")
async def register(user: UserRequest, db: AsyncSession = Depends(get_db)):
    user_exist = await get_user_by_username(db, user.username)
    # 先查找
    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    
    new_user = await create_user(db, user)
    token = await generate_token(db, new_user.id)

    response_data = UserAuthResponse(token= "Bearer " + token, user_info= UserInfoResponse.model_validate(new_user))


    return ok(message="注册成功", data=response_data)



@router.post("/login", summary="登录")
async def login(user: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user.username, user.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    token = await generate_token(db, user.id)

    response_data = UserAuthResponse(token= "Bearer " + token, user_info= UserInfoResponse.model_validate(user))

    return ok(message="登录成功", data=response_data)


# 查用户信息 使用依赖注入
@router.get("/info", summary="获取用户信息")
async def get_user_info(user: User = Depends(get_current_user)):
    
    return ok(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))


# 修改用户信息：验证 token -> 更新（PUT + 请求体）。路由名勿与 crud.update_user_info 同名，否则会递归调用自身。
@router.put("/update", summary="修改用户信息")
async def update_profile(
    user_data: UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    updated_user = await update_user_info(db, user.username, user_data)

    return ok(message="修改用户信息成功", data=UserInfoResponse.model_validate(updated_user))



@router.put("/password", summary="修改密码")
async def update_password(
    password_data: UserPasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    success = await update_user_password(db, user, password_data)
    if not success:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail="旧密码错误")

    return ok(message="修改密码成功")



