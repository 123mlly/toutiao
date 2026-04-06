import os
import redis.asyncio as redis

from redis.commands import json

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "127.0.0.1"),
    port=os.getenv("REDIS_PORT", 6379),
    password=os.getenv("REDIS_PASSWORD", ""),
    db=os.getenv("REDIS_DB", 0),
    decode_responses=True
)

# 获取字符串类型
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

# 读取:字符串、列表和字典
async def get_list_or_dict(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        else:
            return None
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

# 写入:字符串、列表和字典
async def set_cache(key: str, value: any, ex: int = 3600):
    try:
        if(isinstance(value, list) or isinstance(value, dict)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, ex, value)
        return True
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return False