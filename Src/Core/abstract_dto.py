from abc import ABC, abstractmethod
from typing import Self
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.utils import get_fields


"""Абстракция объекта для передачи данных (DTO)"""
class AbstractDto(ABC):
    # Уникальный код DTO
    __unique_code: str

    # Наименование DTO
    __name: str

    @abstractmethod
    def __init__(self):
        super().__init__()
    
    """Поле уникального кода"""
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        vld.is_str(value, "unique_code")
        self.__unique_code = value
    
    """Поле наименования"""
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name")
        self.__name = value
    
    """Метод загрузки полей из переданного словаря"""
    @abstractmethod
    def load(self, data: dict) -> Self:
        vld.is_dict(data, "data")
        fields = get_fields(self)
        marching_keys = [key for key in data if key in fields]

        try:
            for key in marching_keys:
                setattr(self, key, data[key])
        except Exception as e:
            raise OperationException(
                f"Impossible to load data from dict. Error: '{e}'"
            )

        return self
