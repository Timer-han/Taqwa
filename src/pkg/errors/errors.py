class UserNotFoundError(Exception):
    """Пользователь с таким telegram_id не найден"""
    pass

class PermissionDeniedError(Exception):
    """Пользователь не имеет прав для данного действия"""
    pass