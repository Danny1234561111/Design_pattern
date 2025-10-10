from abc import ABC
import uuid
from Src.Core.validator import validator
from typing import Optional


"""
Абстрактный класс для наследования моделей
Содержит в себе только генерацию уникального кода
"""
class abstact_model(ABC):
<<<<<<< HEAD
    __id: str
    __name: str  # Имя должно быть инициализировано
=======
    __unique_code:str
>>>>>>> origin/version_teacher

    def __init__(self) -> None:
        super().__init__()
        self.__id = uuid.uuid4().hex

    """
    Уникальный код
    """
    @property
<<<<<<< HEAD
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        validator.validate(value, str)
        self.__id = value.strip()
=======
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()
    
>>>>>>> origin/version_teacher

    """
    Перегрузка штатного варианта сравнения
    """
    def __eq__(self, value) -> bool:
        if value is  None: return False
        if not isinstance(value, abstact_model): return False

        return self.unique_code == value.unique_code

<<<<<<< HEAD
    def __eq__(self, other) -> bool:
        if isinstance(other, abstact_model):
            return self.id == other.id #Используем геттер
        return False
=======
>>>>>>> origin/version_teacher
