# 新闻分类列表缓存 key
from typing import Any, Dict
from config.cache_conf import get_list_or_dict, set_cache


CATEGORIES_KEY = "news:categories"

#获取缓存分类
async def get_categories_cache():
    return await get_list_or_dict(CATEGORIES_KEY)


# 设置缓存分类
# 7200秒 = 2小时
async def set_categories_cache(categories: list[Dict[str, Any]], exp: int = 7200):
    return await set_cache(CATEGORIES_KEY, categories, exp)