from Src.Core.entity_model import entity_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator
from Src.Core.abstract_dto import abstact_dto

class nomenclature_model(entity_model):
    __group: group_model = None
    __range: range_model = None

    @property
    def group(self) -> group_model:
        return self.__group

    @group.setter
    def group(self, value: group_model):
        validator.validate(value, group_model)
        self.__group = value    

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @staticmethod
    def create(name: str, group: group_model, range: range_model) -> "nomenclature_model":
        validator.validate(name, str)
        item = nomenclature_model()
        item.name = name
        item.group = group
        item.range = range
        return item

    @classmethod
    def from_dto(cls, dto: abstact_dto):
        validator.validate(dto, abstact_dto)
        item = cls.create(dto.name, None, None)
        item.range = dto.range_id
        item.group = dto.group_id
        return item

    def to_dto(self) -> abstact_dto:
        dto = abstact_dto()
        dto.name = self.name
        dto.range_id = self.range.id if self.range else None
        dto.group_id = self.group.id if self.group else None
        return dto