from Src.Core.validator import validator
from Src.Core.entity_model import entity_model
from typing import Optional

class range_model(entity_model):
    __base: Optional["range_model"]
    __conversion_factor: float = 0

    def __init__(self, name: str, conversion_factor: Optional["float"]=None, base: Optional["range_model"] = None):
        self.name = name
        self.conversion_factor = conversion_factor
        self.base = base

    def __eq__(self, other):
        if isinstance(other, range_model):
            return self.name == other.name and self.conversion_factor == other.conversion_factor and self.base == other.base
        return False

    def __hash__(self):
        return hash((self.name, self.conversion_factor, self.base))

    @property
    def base(self) -> Optional["range_model"]:
        return self.__base

    @base.setter
    def base(self, value: Optional["range_model"]):
        if value is not None:
            validator.validate(value, range_model)
        self.__base = value

    @property
    def conversion_factor(self) -> Optional[float]:
        return self.__conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, value: Optional[float]):
        if value is not None:
            validator.validate(value, (int, float))  # Разрешаем int или float
            if value <= 0:
                raise ValueError("Коэффициент пересчета должен быть больше 0.")
        self.__conversion_factor = value

    def to_base(self, value: float) -> float:
        return value * self.conversion_factor

    def from_base(self, value: float) -> float:
        return value / self.conversion_factor

    def get_conversion_factor_to(self, target_unit: "range_model") -> float:
        if self == target_unit:
            return 1.0
        # If we have a base unit, try to convert to that first
        if self.base is not None:
            base_to_target = self.base.get_conversion_factor_to(target_unit)
            if base_to_target is not None:  # Ensure a valid path exists
                return self.conversion_factor * base_to_target
            else:
                return None
        else:
            return None

    @staticmethod
    def create_killogramm(gramm):
        """Создает экземпляр килограмма."""
        return range_model("килограмм",1000, gramm)

    @staticmethod
    def create_gramm():
        """Создает экземпляр грамма."""
        return range_model("грамм")

    @staticmethod
    def create_liter(milliliter):
        """Создает экземпляр литра."""
        return range_model("литр", 1000, milliliter)


    @staticmethod
    def create_milliliter():
        """Создает экземпляр миллилитра."""
        return range_model("миллилитр")

    @staticmethod
    def create_piece():
        """Создает экземпляр штуки."""
        return range_model("штука")

    @staticmethod
    def create(name: str, koef=1,base=None):
        """Метод для создания экземпляров range_model."""
        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        if base is not None and not isinstance(base, range_model):  # Проверка типа base
            raise ValueError("Base must be a range_model instance")

        if not isinstance(koef, (int, float)):
            raise ValueError("Koef must be a number")

        return range_model(name, koef, base)