from Src.Core.validator import validator
from Src.Core.entity_model import entity_model
from typing import Optional, TYPE_CHECKING
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.range_model import range_model

class nomenclature_model(entity_model):
    __full_name: str = ""
    __group: nomenclature_group_model=None
    __unit: range_model = None

    def __eq__(self, other):
        if isinstance(other, nomenclature_model):
            return self.name == other.name and self.full_name == other.full_name and self.group == other.group and self.unit == other.unit
        return False

    def __hash__(self):
        return hash((self.name, self.full_name, self.group, self.unit))

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        validator.validate(value, str)
        if len(value) > 255:
            raise ValueError("Полное наименование не должно превышать 255 символов.")
        self.__full_name = value.strip()

    @property
    def group(self) -> nomenclature_group_model:
        return self.__group

    @group.setter
    def group(self, value: nomenclature_group_model):

        from Src.Models.nomenclature_group_model import nomenclature_group_model
        validator.validate(value, nomenclature_group_model)
        self.__group = value

    @property
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        validator.validate(value, range_model)
        self.__unit = value