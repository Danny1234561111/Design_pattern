from typing import Self
from src.core.abstract_dto import AbstractDto


"""DTO для модели NomenclatureGroupModel"""
class NomenclatureGroupDto(AbstractDto):
    
    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
