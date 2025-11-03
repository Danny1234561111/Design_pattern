from typing import Optional
from src.core.abstract_model import AbstractModel
from src.core.validator import Validator as vld
from src.dtos.storage_dto import StorageDto  # Обязательно импортируйте DTO
from src.singletons.repository import Repository

"""Модель склада"""
class StorageModel(AbstractModel):
    # Наименование склада
    __name: Optional[str] = None
    __address: Optional[str] = None

    def __init__(self, name: Optional[str] = None,address: Optional[str] = None):
        super().__init__()
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address

    """Поле наименования"""
    @property
    def name(self) -> Optional[str]:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "address", len_=255)  # Условие длины можно изменить по необходимости
        self.__name = value.strip()
    @property
    def address(self) -> Optional[str]:
        return self.__address
    
    @name.setter
    def address(self, value: str):
        vld.is_str(value, "address", len_=255)  # Условие длины можно изменить по необходимости
        self.__address = value.strip()

    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: StorageDto,repo: Repository) -> 'StorageModel':
        return StorageModel(
            name=dto.name,
            address = dto.address
        )