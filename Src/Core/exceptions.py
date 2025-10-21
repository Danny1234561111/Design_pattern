# Src/Core/exceptions.py

class ParamException(Exception):
    """Исключение, вызываемое при некорректных параметрах."""
    
    def __init__(self, message):
        super().__init__(message)


class WrongTypeException(ParamException):
    """Исключение, вызываемое при неверном типе параметра."""
    
    def __init__(self, expected_type, actual_type):
        message = f"Ожидался тип {expected_type}, но получен {actual_type}."
        super().__init__(message)
