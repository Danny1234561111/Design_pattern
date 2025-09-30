from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model
from typing import Optional, TYPE_CHECKING
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.range_model import range_model

class nomenclature_model(abstact_model):
    __name: str = ""
    __full_name: str = ""
    __group: nomenclature_group_model
    __unit: range_model

    def __init__(self, name: str, full_name: str, group: nomenclature_group_model, unit: range_model):
        super().__init__()
        self.name = name
        self.full_name = full_name
        self.group = group
        self.unit = unit

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value.strip()

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

        from Src.Models.range_model import range_model
        validator.validate(value, range_model)
        self.__unit = value
