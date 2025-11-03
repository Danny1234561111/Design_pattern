from typing import Optional, Self
from src.core.abstract_model import AbstractModel
from src.dtos.nomenclature_group_dto import NomenclatureGroupDto
from src.singletons.repository import Repository


"""Модель для характеристики группы номенклатуры"""
class NomenclatureGroupModel(AbstractModel):
    # Наименование (50)
    # Наследуется от AbstractModel

    def __init__(
        self,
        name: Optional[str] = None
    ):
        super().__init__()
        if name is not None:
            self.name = name
    
    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: NomenclatureGroupDto, repo: Repository) -> Self:
        return NomenclatureGroupModel(name=dto.name)
