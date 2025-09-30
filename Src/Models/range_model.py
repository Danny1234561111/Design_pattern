from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model
from typing import Optional

class range_model(abstact_model):
    __name: str = ""
    __base_unit: Optional["range_model"]
    __conversion_factor: float = 1.0

    def __init__(self, name: str, conversion_factor: float, base_unit: Optional["range_model"] = None):
        super().__init__()
        self.name = name
        self.conversion_factor = conversion_factor
        self.base_unit = base_unit

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value.strip()

    @property
    def base_unit(self) -> Optional["range_model"]:
        return self.__base_unit

    @base_unit.setter
    def base_unit(self, value: Optional["range_model"]):
        if value is not None:
            validator.validate(value, range_model)
        self.__base_unit = value

    @property
    def conversion_factor(self) -> float:
        return self.__conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, value: float):
        validator.validate(value, float)
        if value <= 0:
            raise ValueError("Коэффициент пересчета должен быть больше 0.")
        self.__conversion_factor = value

    def to_base_unit(self, value: float) -> float:
        return value * self.conversion_factor

    def from_base_unit(self, value: float) -> float:
        return value / self.conversion_factor

    def get_conversion_factor_to(self, target_unit: "range_model") -> float:
        if self == target_unit:
            return 1.0
        # If we have a base unit, try to convert to that first
        if self.base_unit is not None:
            base_to_target = self.base_unit.get_conversion_factor_to(target_unit)
            if base_to_target is not None:  # Ensure a valid path exists
                return self.conversion_factor * base_to_target
            else:
                return None # No conversion path exists
        else:
            return None # If there's no base unit then can't convert.