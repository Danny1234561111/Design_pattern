from abc import ABC
import uuid
from Src.Core.validator import validator

class abstact_model(ABC):
    __unique_code: str
    __name: str

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()

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
            return self.__unique_code == other.__unique_code
        return False
