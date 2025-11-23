from typing import Optional
from datetime import datetime
from src.core.abstract_model import AbstractModel
from src.core.validator import Validator as vld
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.storage_model import StorageModel
from src.dtos.transaction_dto import TransactionDto 
from src.singletons.repository import Repository

class Ost:

    # Номенклатура
    __nomenclature: NomenclatureModel


    # Количество
    __quantity: float

    # Единица измерения
    __measure_unit: MeasureUnitModel
    __storage: StorageModel

    def __init__(self, 
                 nomenclature: NomenclatureModel,
                 quantity: float,
                 measure_unit: MeasureUnitModel,
                 storage: StorageModel):
        
        self.nomenclature = nomenclature
        self.quantity = quantity
        self.measure_unit = measure_unit
        self.storage = storage

    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: str):
        vld.validate(NomenclatureModel,value, "nomenclature")
        self.__name = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        vld.validate(float,value, "quantity")
        self.__quantity = value
    
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self.__measure_unit

    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(MeasureUnitModel,value, "measure_unit")
        self.__measure_unit = value
    
    @property
    def storage(self) -> StorageModel:
        return self.__storage

    @storage.setter
    def storage(self, value: StorageModel):
        vld.validate(StorageModel,value, "storage")
        self.__storage = value