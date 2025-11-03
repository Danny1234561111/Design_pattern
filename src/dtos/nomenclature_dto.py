from typing import Self
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto


"""DTO для модели NomenclatureModel"""
class NomenclatureDto(AbstractDto):
    # Группа номенклатуры
    __group: str = ""

    # Единица измерения
    __measure_unit: str = ""

    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
    
    """Поле группы номенклатуры"""
    @property
    def group(self) -> str:
        return self.__group
    
    @group.setter
    def group(self, value: str):
        vld.is_str(value, "group name")
        self.__group = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> str:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: str):
        vld.is_str(value, "measure unit name")
        self.__measure_unit = value
