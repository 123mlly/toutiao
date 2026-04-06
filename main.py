import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# 必须在导入 routes / config（会读 os.environ）之前加载。
# override=True：终端 / IDE 里已存在的同名变量会被 .env 覆盖，避免一直读到旧值。
load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from routes import aichat_router, favorite_router, history_router, news_router, users_router
from utils.register_exception import register_exception
from utils.response import fail


logger = logging.getLogger("aitoutiao")


def _is_debug() -> bool:
    return os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")


app = FastAPI(title="aitoutiao")

# 注册异常处理
register_exception(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有源
    allow_credentials=True, # 允许携带凭证 cookies, headers, etc.
    allow_methods=["*"], # 允许所有方法 GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"], # 允许所有头 Content-Type, Authorization, etc.
)

@app.get("/")
def read_root():
    return {"message": "ok"}


# 注册路由 路由优先级：先新闻，后用户
app.include_router(news_router)
app.include_router(users_router)
app.include_router(favorite_router)
app.include_router(history_router)
app.include_router(aichat_router)