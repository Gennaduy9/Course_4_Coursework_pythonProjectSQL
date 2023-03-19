class BaseServiceError(Exception):
    code = 500
    message = "Unexpected error"


class ItemNotFound(BaseServiceError):
    code = 404
    message = "Не найдено!"


class UserAlreadyExists(BaseServiceError):
    code = 400
    message = "Такой пользователь уже существует!"
