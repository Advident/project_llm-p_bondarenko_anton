from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """Бизнес-логика работы с чатом и историей."""

    def __init__(
        self,
        chat_repo: ChatMessagesRepository,
        openrouter_client: OpenRouterClient,
    ) -> None:
        self._chat_repo = chat_repo
        self._openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        """Отправляет запрос в LLM с контекстом истории и сохраняет диалог."""
        messages: list[dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        history = await self._chat_repo.get_last_messages(user_id=user_id, limit=max_history)
        for item in history:
            messages.append({"role": item.role, "content": item.content})

        messages.append({"role": "user", "content": prompt})

        await self._chat_repo.add_message(user_id=user_id, role="user", content=prompt)

        answer = await self._openrouter_client.chat_completion(
            messages=messages,
            temperature=temperature,
        )

        await self._chat_repo.add_message(user_id=user_id, role="assistant", content=answer)
        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> list[ChatMessage]:
        """Возвращает историю сообщений пользователя."""
        return await self._chat_repo.get_last_messages(user_id=user_id, limit=limit)

    async def clear_history(self, user_id: int) -> None:
        """Очищает историю сообщений пользователя."""
        await self._chat_repo.clear_history(user_id=user_id)