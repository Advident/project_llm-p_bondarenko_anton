from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Схема запроса к LLM."""

    prompt: str = Field(min_length=1, max_length=10000)
    system: str | None = Field(default=None, max_length=5000)
    max_history: int = Field(default=10, ge=0, le=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    """Схема ответа от LLM."""

    answer: str


class ChatMessagePublic(BaseModel):
    """Публичная схема сообщения истории."""

    id: int
    role: str
    content: str
    created_at: str