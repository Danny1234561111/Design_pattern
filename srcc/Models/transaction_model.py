from typing import Optional
from datetime import datetime
from src.core.abstract_model import AbstractModel
from src.core.validator import Validator as vld
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.storage_model import StorageModel
from src.dtos.transaction_dto import TransactionDto 
from src.singletons.repository import Repository

class TransactionModel(AbstractModel):
    # Дата транзакции
    __date: Optional[datetime] = None

    # Уникальный номер транзакции
    __unique_number: Optional[str] = None

    # Номенклатура
    __nomenclature: Optional[NomenclatureModel] = None

    # Склад
    __storage: Optional[StorageModel] = None

    # Количество
    __quantity: Optional[float] = None

    # Единица измерения
    __measure_unit: Optional[MeasureUnitModel] = None
    
    # Имя транзакции
    __name: Optional[str] = None

    def __init__(self, 
                 date: Optional[datetime] = None,
                 unique_number: Optional[str] = None,
                 nomenclature: Optional[NomenclatureModel] = None,
                 storage: Optional[StorageModel] = None,
                 quantity: Optional[float] = None,
                 measure_unit: Optional[MeasureUnitModel] = None,
                 name: Optional[str] = None):
        super().__init__()
        self.date = date
        self.unique_number = unique_number
        self.nomenclature = nomenclature
        self.storage = storage
        self.quantity = quantity
        self.measure_unit = measure_unit
        self.name = name  # Устанавливаем имя
    
    """Поле имени"""
    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name", len_=255)
        self.__name = value.strip()

    @staticmethod
    def from_dto(dto: TransactionDto, repo: Repository) -> 'TransactionModel':
        nomenclature = repo.get_by_name(dto.nomenclature_name)
        if nomenclature is None:
            raise ValueError(f"Nomenclature '{dto.nomenclature_name}' not found in repository.")

        storage = repo.get_by_name(dto.storage_name)
        if storage is None:
            raise ValueError(f"Storage '{dto.storage_name}' not found in repository.")

        measure_unit = repo.get_by_name(dto.measure_unit_name)
        if measure_unit is None:
            raise ValueError(f"Measure unit '{dto.measure_unit_name}' not found in repository.")

        # Убедитесь, что уникальный номер передается, если есть
        unique_number = dto.name  # Используем поле name как уникальный номер, если оно предоставлено

        return TransactionModel(
            date=datetime.strptime(dto.datetime, "%Y-%m-%d"),
            unique_number=unique_number,
            nomenclature=nomenclature,
            storage=storage,
            quantity=dto.count,
            measure_unit=measure_unit,
            name=dto.name  
        )