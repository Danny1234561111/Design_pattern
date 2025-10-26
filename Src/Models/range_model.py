from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Core.abstract_dto import abstact_dto

class range_model(entity_model):
    __value: int = 1
    __base: 'range_model' = None

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Некорректный аргумент!")
        self.__value = value

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        self.__base = value

    @staticmethod
    def create(name: str, value: int, base=None):
        validator.validate(name, str)
        validator.validate(value, int)

        inner_base = None
        if base is not None:
            validator.validate(base, range_model)
            inner_base = base

        item = range_model()
        item.name = name
        item.base = inner_base
        item.value = value
        return item

    def to_dto(self) -> abstact_dto:
        dto = abstact_dto()
        dto.name = self.name
        dto.id = self.id  # Предположим, что self.id существует и представляет идентификатор
        dto.value = self.value
        dto.base_id = self.base.id if self.base else None
        return dto

    @classmethod
    def from_dto(cls, dto: abstact_dto):
        instance = cls()
        instance.name = dto.name
        instance.value = dto.value
        instance.base = dto.base_id  # Задаем базу используя ID
        return instance