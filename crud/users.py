from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from models.users import User, UserToken
from schemas.users import UserPasswordRequest, UserRequest, UserUpdateRequest
from utils.security import hash_password, verify_password


async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserRequest):
    hashed_password = hash_password(user.password)

    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user) # 刷新对象，更新对象的属性
    return new_user



# 生成token
async def generate_token(db: AsyncSession, user_id: int):
    #  生成token + 过期时间 -> 查询数据库是否有token
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
        await db.refresh(user_token)

    return token


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


# 根据token获取用户信息
async def get_user_by_token(db: AsyncSession, token: str):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()

    if not db_token:
        return None
    if db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 更新用户信息
async def update_user_info(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_none=True,
        exclude_unset=True
    ))

    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 获取用户信息
    updated_user = await get_user_by_username(db, username)


    return updated_user


# 修改密码 验证就密码-> 新密码加密 -> 修改密码
async def update_user_password(db: AsyncSession, user: User, password_data: UserPasswordRequest):

    if not verify_password(password_data.old_password, user.password):
        return False
    
    new_hash_password = hash_password(password_data.new_password)

    user.password = new_hash_password
    #db.add(user)
    await db.commit()
    await db.refresh(user)
    return True



