from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessagesRepository:
    """Репозиторий для работы с сообщениями чата."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Сохраняет сообщение пользователя или модели."""
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_last_messages(self, user_id: int, limit: int) -> list[ChatMessage]:
        """Возвращает последние N сообщений пользователя."""
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        messages = list(result.scalars().all())
        messages.reverse()
        return messages

    async def clear_history(self, user_id: int) -> None:
        """Удаляет всю историю пользователя."""
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()