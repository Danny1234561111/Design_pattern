from typing import Optional, Self
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.dtos.Ingredient_dto import IngredientDto
from src.models.nomenclature_model import NomenclatureModel
from src.models.measure_unit_model import MeasureUnitModel
from src.singletons.repository import Repository


"""Модель ингредиента рецепта"""
class IngredientModel(AbstractModel):
    # Наименование (наследуется от AbstractModel)

    # Номенклатура, описывающая ингредиент
    __nomenclature: NomenclatureModel

    # Единица измерения, в которой указывается count
    __measure_unit: MeasureUnitModel

    # Количество ингредиента (в measure_unit)
    __count: int
    
    def __init__(
        self,
        nomenclature: Optional[NomenclatureModel],
        measure_unit: Optional[MeasureUnitModel],
        count: Optional[int],
    ):
        super().__init__()
        if nomenclature is not None:
            self.nomenclature = nomenclature
        if measure_unit is not None:
            self.measure_unit = measure_unit
        if count is not None:
            self.count = count
    
    """Поле наименования"""
    @property
    def name(self) -> str:
        return f"ингредиент '{self.nomenclature.name}'"

    """Поле номенклатуры"""
    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        vld.validate(value, NomenclatureModel, "nomenclature")
        self.__nomenclature = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(value, MeasureUnitModel, "measure_unit")
        self.__measure_unit = value
    
    """Поле количества ингредиента"""
    @property
    def count(self) -> int:
        return self.__count
    
    @count.setter
    def count(self, value: int):
        vld.is_int(value, "count")
        self.__count = value
    
    """Универсальный фабричный метод"""
    @staticmethod
    def create(
        nomenclature: NomenclatureModel,
        measure_unit: MeasureUnitModel,
        count: int,
    ) -> Self:
        return IngredientModel(nomenclature, measure_unit, count)
    
    """Фабричный метод из DTO"""
    def from_dto(dto: IngredientDto, repo: Repository) -> Self:
        nomenclature = repo.get_by_name(dto.nomenclature)
        measure_unit = repo.get_by_name(dto.measure_unit)
        return IngredientModel(
            nomenclature=nomenclature,
            measure_unit=measure_unit,
            count=dto.count,
        )
