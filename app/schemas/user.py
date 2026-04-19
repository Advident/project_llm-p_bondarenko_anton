from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    """Публичная схема пользователя."""

    id: int
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)