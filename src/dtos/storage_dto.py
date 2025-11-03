from typing import Self
from src.core.abstract_dto import AbstractDto
from src.core.validator import Validator as vld
class StorageDto(AbstractDto):
    name: str
    address: str
    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        super().load(data)
        self.name = data["name"]
        self.address = data["address"]
        return self