from typing import Self
from Src.Core.validator import validator
from Src.Core.abstract_dto import abstact_dto


"""DTO для модели IngredientModel"""
class IngredientDto(abstact_dto):
    # Номенклатура
    __nomenclature: str

    # Единица измерения
    __measure_unit: str

    # Количество ингредиента
    __count: int

    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
    
    """Поле номенклатуры"""
    @property
    def nomenclature(self) -> str:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: str):
        validator.is_str(value, "nomenclature")
        self.__nomenclature = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> str:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: str):
        validator.is_str(value, "measure_unit")
        self.__measure_unit = value
    
    """Поле количества ингредиента"""
    @property
    def count(self) -> int:
        return self.__count
    
    @count.setter
    def count(self, value: int):
        validator.is_int(value, "count")
        self.__count = value