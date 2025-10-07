from abc import ABC
import uuid
from Src.Core.validator import validator
from typing import Optional


class abstact_model(ABC):
    __id: str
    __name: str  # Имя должно быть инициализировано

    def __init__(self) -> None:
        super().__init__()
        self.__id = uuid.uuid4().hex

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        validator.validate(value, str)
        self.__id = value.strip()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        if len(value) > 50:
            raise ValueError("Имя не должно превышать 50 символов.")
        self.__name = value.strip()

    def __eq__(self, other) -> bool:
        if isinstance(other, abstact_model):
            return self.id == other.id #Используем геттер
        return False