from typing import Self
from src.core.abstract_dto import AbstractDto
from src.core.validator import Validator as vld

class TransactionDto(AbstractDto):
    datetime: str
    nomenclature_name: str
    storage_name: str
    count: float
    measure_unit_name: str
    name: str  # Добавлено поле для имени транзакции
    
    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)

    def load(self, data) -> Self:
        super().load(data)
        self.datetime = data["datetime"]
        self.nomenclature_name = data["nomenclature_name"]
        self.storage_name = data["storage_name"]
        self.count = data["count"]
        self.measure_unit_name = data["measure_unit_name"]
        return self