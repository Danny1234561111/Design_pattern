"""Исключение при непрохождении аргументом валидации"""
class InvalidValueException(ValueError):
    pass


"""Исключение при неверном типе аргумента"""
class WrongTypeException(TypeError):
    pass


"""Исключение при неверно переданном аргументе функции"""
class ParamException(Exception):
    pass


"""Исключение при нарушении логики бизнес-операции"""
class OperationException(Exception):
    pass


"""Ошибка прокси"""
class ProxyError(Exception):
    pass
