from abc import ABC, abstractmethod
from src.core.validator import Validator as vld
from src.core.response_format import ResponseFormat


"""Абстрактный класс для формирования ответов"""
class AbstractResponse(ABC):
    
    @abstractmethod
    def __init__(self):
        super().__init__()

    """Сформировать нужный ответ"""
    @abstractmethod
    def build(self, data: list, format: ResponseFormat) -> str:
        vld.validate(format, ResponseFormat, "format")
        vld.is_list_of_same(data, "list of models", True)

        return ""
