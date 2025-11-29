from abc import ABC, abstractmethod
from src.core.validator import Validator
from abc import ABC
from src.core.validator import Validator
from src.core.exceptions import OperationException
from src.core.event_type import event_type


"""
Абстрактный класс для обработки логики
"""
class abstract_logic(ABC):
    __error_text:str = ""

    """
    Описание ошибки
    """
    @property
    def error_text(self) -> str:
        return  self.__error_text.strip()
    
    
    @error_text.setter
    def error_text(self, message: str):
        Validator.validate(message, str)
        self.__error_text = message.strip()

    """
    Флаг. Есть ошибка
    """
    @property
    def is_error(self) -> bool:
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    """
    Метод для загрузки и обработки исключений
    """
    def set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    """
    Обработка события
    """
    def handle(self,  event: str, params):
        Validator.validate(event, str)
        events =  event_type.events()
        if event not in events:
            raise OperationException(f"{events} - не является событием!")