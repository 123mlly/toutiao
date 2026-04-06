from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """单条对话，与 OpenAI Chat Completions messages 项一致。"""

    role: Literal["system", "user", "assistant", "tool"] = Field(
        ..., description="system / user / assistant / tool"
    )
    content: str = Field(..., description="该轮文本内容")

    model_config = ConfigDict(populate_by_name=True)


class ChatRequest(BaseModel):
    """前端传入完整多轮上下文（含 system、历史 user/assistant 与本轮 user）。"""

    messages: list[ChatMessage] = Field(
        ...,
        min_length=1,
        description="对话消息列表，按时间顺序",
    )

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
