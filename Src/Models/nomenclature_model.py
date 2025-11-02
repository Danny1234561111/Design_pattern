from typing import Optional, Self
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.dtos.nomenclature_dto import NomenclatureDto
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.singletons.repository import Repository


"""Модель номенклатуры"""
class NomenclatureModel(AbstractModel):
    # Наименование (255)
    __name: Optional[str] = None

    # Группа номенклатуры
    __group: Optional[NomenclatureGroupModel] = None

    # Единица измерения
    __measure_unit: Optional[MeasureUnitModel] = None

    def __init__(
        self,
        name: Optional[str] = None,
        group: Optional[NomenclatureGroupModel] = None,
        unit: Optional[MeasureUnitModel] = None,
    ):
        super().__init__()
        if name is not None:
            self.name = name
        if group is not None:
            self.group = group
        if unit is not None:
            self.measure_unit = unit

    """Поле наименования"""
    @property
    def name(self) -> Optional[str]:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name", len_=255)
        self.__name = value.strip()
    
    """Поле группы номенклатуры"""
    @property
    def group(self) -> Optional[NomenclatureGroupModel]:
        return self.__group
    
    @group.setter
    def group(self, value: Optional[NomenclatureGroupModel]):
        vld.validate(value, NomenclatureGroupModel, "group", True)
        self.__group = value
    
    """Поле, хранящее объект единицы измерения"""
    @property
    def measure_unit(self) -> Optional[MeasureUnitModel]:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: Optional[MeasureUnitModel]):
        vld.validate(value, MeasureUnitModel, "measure_unit", True)
        self.__measure_unit = value
    
    """Универсальный фабричный метод"""
    @staticmethod
    def create(
        name: Optional[str] = None,
        group: Optional[NomenclatureGroupModel] = None,
        unit: Optional[MeasureUnitModel] = None,
    ) -> Self:
        return NomenclatureModel(name, group, unit)
    
    """Фабричный метод из DTO"""
    def from_dto(dto: NomenclatureDto, repo: Repository) -> Self:
        group = repo.get_by_name(dto.group)
        unit = repo.get_by_name(dto.measure_unit)
        return NomenclatureModel(
            name=dto.name,
            group=group,
            unit=unit,
        )