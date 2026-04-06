import json
import os
import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import APIError, AsyncOpenAI

from schemas.aichat import ChatRequest
from utils.response import fail

API_END_POINT = os.getenv("API_END_POINT")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

logger = logging.getLogger("aichat")

router = APIRouter(prefix="/api/aichat", tags=["聊天机器人接口"])


@router.post("/chat", summary="AI聊天")
async def chat(request: ChatRequest):
    if not API_KEY or not MODEL:
        return fail(message="未配置 API_KEY / MODEL", status_code=500)

    payload_messages = [m.model_dump() for m in request.messages]

    async def sse_proxy():
        try:
            async with AsyncOpenAI(
                api_key=API_KEY, base_url=API_END_POINT
            ) as client:
                stream = await client.chat.completions.create(
                    model=MODEL,
                    messages=payload_messages,
                    stream=True,
                )
                async for chunk in stream:
                    yield f"data: {chunk.model_dump_json()}\n\n"
                yield "data: [DONE]\n\n"
        except APIError as e:
            payload = json.dumps({"error": str(e)}, ensure_ascii=False)
            logger.error(payload)
            yield f"data: {payload}\n\n"

    return StreamingResponse(
        sse_proxy(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
