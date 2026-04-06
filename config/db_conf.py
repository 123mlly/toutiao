import os
from collections.abc import AsyncIterator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    _db_url = DATABASE_URL
    if not _db_url.startswith("mysql+aiomysql"):
        raise ValueError("DATABASE_URL must use scheme mysql+aiomysql for async aiomysql")
else:
    _db_url = URL.create(
        drivername="mysql+aiomysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "news_app"),
    )

async_engine = create_async_engine(
    _db_url,
    echo=os.getenv("SQL_ECHO", "").lower() in ("1", "true", "yes"),
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
    pool_pre_ping=True,
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


async def close_db() -> None:
    await async_engine.dispose()


get_db = get_session
