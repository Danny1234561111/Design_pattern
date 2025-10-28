from typing import Dict, Any
from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Core.abstract_dto import abstact_dto

class ReceiptModel(entity_model):
    def __init__(self):
        super().__init__()
        self.company: Dict[str, Any] = {}  # Словарь для хранения информации о компании
        self.default_receipt: Dict[str, Any] = {}  # Словарь для хранения информации о дефолтном чеке

    def convert(self, data: dict) -> None:
        """Конвертация данных из словаря."""
        validator.validate(data, dict)

        self.company = data.get("company", {})
        self.default_receipt = data.get("default_receipt", {})

    def to_dto(self) -> abstact_dto:
        """Преобразование в DTO (Data Transfer Object)."""
        dto = abstact_dto()
        dto.company_name = self.company.get('name', "")
        dto.company_inn = self.company.get('inn', "")
        dto.default_receipt_name = self.default_receipt.get('name', "")
        # Здесь также можно добавить преобразование других частей default_receipt
        return dto