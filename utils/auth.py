# 整合 根据token获取用户信息

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Header, Depends, status
from config.db_conf import get_db
from crud.users import get_user_by_token

async def get_current_user(
    authorization: str | None = Header(
        ..., description="Authorization: Bearer <token>", alias="Authorization"
    ),
    db: AsyncSession = Depends(get_db),
):
    if not authorization or not authorization.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少 Authorization 头",
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization 格式应为: Bearer <token>",
        )
    token = parts[1]

    user = await get_user_by_token(db, token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌")
    
    return user

