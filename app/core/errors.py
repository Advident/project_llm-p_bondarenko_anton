class AppError(Exception):
    """Базовая доменная ошибка приложения."""


class ConflictError(AppError):
    """Ошибка конфликта данных."""


class UnauthorizedError(AppError):
    """Ошибка аутентификации."""


class ForbiddenError(AppError):
    """Ошибка авторизации / недостатка прав."""


class NotFoundError(AppError):
    """Ошибка отсутствия объекта."""


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса."""