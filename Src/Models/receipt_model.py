from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Core.abstract_dto import abstact_dto

class receipt_model(entity_model):
    __portions: int = 1
    __steps: list = []
    __composition: list = []
    __cooking_time: str = ""

    @property
    def portions(self) -> int:
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        validator.validate(value, int)
        self.__portions = value

    @property
    def steps(self) -> list:
        return self.__steps

    @property
    def composition(self) -> list:
        return self.__composition

    @property
    def cooking_time(self) -> str:
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: str):
        validator.validate(value, str)
        self.__cooking_time = value.strip()

    @staticmethod
    def create(name: str, cooking_time: str, portions: int) -> "receipt_model":
        item = receipt_model()
        item.name = name
        item.cooking_time = cooking_time
        item.portions = portions
        return item

    def to_dto(self) -> abstact_dto:
        dto = abstact_dto()
        dto.portions = self.portions
        dto.cooking_time = self.cooking_time
        dto.steps = self.steps
        return dto

    @classmethod
    def from_dto(cls, dto: abstact_dto):
        instance = cls()
        instance.portions = dto.portions
        instance.cooking_time = dto.cooking_time
        instance.steps = dto.steps
        return instance