from typing import List, Dict, Any # Добавил Any для гибкости типов значений
from datetime import datetime
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.models.transaction_model import TransactionModel
from src.models.ost_model import Ost
from src.models.measure_unit_model import MeasureUnitModel
from src.models.storage_model import StorageModel
from src.models.nomenclature_model import NomenclatureModel


class TbsLineOst:
    _nomenclature: NomenclatureModel
    _measure_unit: MeasureUnitModel
    _storage: StorageModel
    _ost: List[float]
    
    def __init__(self, transaction: TransactionModel):
        self.nomenclature = transaction.nomenclature
        # !!! ИСПРАВЛЕНИЕ ОШИБКИ TypeError: cannot unpack non-iterable NoneType object !!!
        base_unit, _ = self.nomenclature.measure_unit.get_base_unit()
        self.measure_unit = base_unit
        self.storage = transaction.storage
        self._ost = []

    @property
    def quantity(self) -> float:
        return sum(self._ost)

    def add(self, trans: TransactionModel):
        vld.validate(trans, TransactionModel, "transaction")

        if self.nomenclature != trans.nomenclature:
            raise OperationException(
                f"Nomenclature of transaction must be "
                f"'{self.nomenclature.name}', not '{trans.nomenclature.name}'"
            )
        
        # !!! Убедитесь, что у TransactionModel есть атрибут 'measure_unit' !!!
        base_unit_trans, coef = trans.measure_unit.get_base_unit()
        if self.measure_unit != base_unit_trans:
            raise OperationException(
                f"Impossible to compare measure unit of transaction "
                f"('{trans.measure_unit.name}'), which super base unit is "
                f"'{base_unit_trans.name}', and base unit of tbs line: "
                f"'{self.measure_unit.name}'"
            )

        # !!! Убедитесь, что у TransactionModel есть атрибут 'quantity' (не 'quantity') !!!
        quantity = trans.quantity * coef 
        
        # !!! Убедитесь, что у TransactionModel есть атрибут 'datetime' (не 'date') !!!
        self._ost.append(quantity)
    def add_ost(self, trans: dict):
        vld.validate(trans, dict, "ost")

        if self.nomenclature != trans.nomenclature:
            raise OperationException(
                f"Nomenclature of transaction must be "
                f"'{self.nomenclature.name}', not '{trans.nomenclature.name}'"
            )
        
        # !!! Убедитесь, что у TransactionModel есть атрибут 'measure_unit' !!!
        base_unit_trans, coef = trans.measure_unit.get_base_unit()
        if self.measure_unit != base_unit_trans:
            raise OperationException(
                f"Impossible to compare measure unit of transaction "
                f"('{trans.measure_unit.name}'), which super base unit is "
                f"'{base_unit_trans.name}', and base unit of tbs line: "
                f"'{self.measure_unit.name}'"
            )

        # !!! Убедитесь, что у TransactionModel есть атрибут 'quantity' (не 'quantity') !!!
        quantity = trans.quantity * coef 
        
        # !!! Убедитесь, что у TransactionModel есть атрибут 'datetime' (не 'date') !!!
        self._ost.append(quantity)

    # --- НОВЫЕ МЕТОДЫ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ ВНУТРИ КЛАССА TBSLINE ---
    def to_display_dict(self) -> Dict[str, Any]:
        """
        Возвращает данные строки ОСВ в виде словаря с русскими названиями
        и в порядке, удобном для отображения.
        """
        return {
            "Имя номенклатуры": self.nomenclature,
            "Единица измерения": self.measure_unit,
            "Склад": self.storage,
            "Остаток": round(self.quantity, 3),
        }

    def to_display_data(self) -> Dict[str, Any]:
        """
        Возвращает данные строки ОСВ в виде словаря с русскими названиями
        и в порядке, удобном для отображения.
        """
        if (round(self.quantity, 3)==0):
            return {}
        return {
            "Имя номенклатуры": self.nomenclature.name,
            "Единица измерения": self.measure_unit.name,
            "Склад": self.storage,
            "Остаток": round(self.quantity, 3),
        }
    @staticmethod
    def get_display_headers() -> List[str]:
        """
        Возвращает список заголовков столбцов в желаемом порядке для отображения.
        """
        return [
            "Имя номенклатуры",
            "Единица измерения",
            "Склад",
            "Остаток"
        ]