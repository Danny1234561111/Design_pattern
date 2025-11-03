from typing import Self, Optional, Union
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto


"""DTO для модели MeasureUnitModel"""
class MeasureUnitDto(AbstractDto):
    # Коэффициент пересчёта
    __coefficient: float = 1.0

    # Базовая единица измерения
    __base_unit: Optional[str] = None

    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
    
    """Поле коэффициента пересчёта"""
    @property
    def coefficient(self) -> float:
        return self.__coefficient
    
    @coefficient.setter
    def coefficient(self, value: Union[int, float]):
        vld.is_number(value, "coefficient")
        self.__coefficient = float(value)
    
    """Базовая единица измерения"""
    @property
    def base_unit(self) -> Optional[str]:
        return self.__base_unit
    
    @base_unit.setter
    def base_unit(self, value: Optional[str]):
        vld.is_str(value, "base unit name", could_be_none=True)
        self.__base_unit = value
