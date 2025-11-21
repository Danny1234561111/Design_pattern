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
    __nomenclature: Optional[NomenclatureModel] = None


    # Количество
    __quantity: Optional[float] = None

    # Единица измерения
    __measure_unit: Optional[MeasureUnitModel] = None

    def __init__(self, 
                 nomenclature: Optional[NomenclatureModel] = None,
                 quantity: Optional[float] = None,
                 measure_unit: Optional[MeasureUnitModel] = None):
        self.nomenclature = nomenclature
        self.quantity = quantity
        self.measure_unit = measure_unit