from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessagesRepository
from app.repositories.users import UsersRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет SQLAlchemy AsyncSession."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_users_repo(
    session: AsyncSession = Depends(get_db_session),
) -> UsersRepository:
    """Предоставляет репозиторий пользователей."""
    return UsersRepository(session=session)


async def get_chat_repo(
    session: AsyncSession = Depends(get_db_session),
) -> ChatMessagesRepository:
    """Предоставляет репозиторий сообщений."""
    return ChatMessagesRepository(session=session)


def get_openrouter_client() -> OpenRouterClient:
    """Предоставляет клиент OpenRouter."""
    return OpenRouterClient()


async def get_auth_usecase(
    users_repo: UsersRepository = Depends(get_users_repo),
) -> AuthUseCase:
    """Предоставляет usecase аутентификации."""
    return AuthUseCase(users_repo=users_repo)


async def get_chat_usecase(
    chat_repo: ChatMessagesRepository = Depends(get_chat_repo),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    """Предоставляет usecase чата."""
    return ChatUseCase(
        chat_repo=chat_repo,
        openrouter_client=openrouter_client,
    )


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    """Извлекает user_id из JWT access token."""
    try:
        payload = decode_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise UnauthorizedError("Token payload does not contain sub")
        return int(sub)
    except (ValueError, UnauthorizedError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc