# src\logics\tbs_line.py
from typing import List, Dict, Any # Добавил Any для гибкости типов значений
from datetime import datetime
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.models.transaction_model import TransactionModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel


class TbsLine:
    _nomenclature: NomenclatureModel
    _measure_unit: MeasureUnitModel
    _counts_before_start: List[float]
    _counts_before_end: List[float]
    
    def __init__(self, transaction: TransactionModel):
        self.nomenclature = transaction.nomenclature
        # !!! ИСПРАВЛЕНИЕ ОШИБКИ TypeError: cannot unpack non-iterable NoneType object !!!
        base_unit, _ = self.nomenclature.measure_unit.get_base_unit()
        self.measure_unit = base_unit
        self._counts_before_start = []
        self._counts_before_end = []

    # --- Property методы (без изменений) ---
    @property
    def nomenclature(self) -> NomenclatureModel:
        return self._nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        vld.validate(value, NomenclatureModel, "nomenclature")
        self._nomenclature = value
    
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self._measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(value, MeasureUnitModel, "measure_unit")
        self._measure_unit = value
    
    @property
    def start_count(self) -> float:
        return sum(self._counts_before_start)
    
    @property
    def income(self) -> float:
        return sum(value for value in self._counts_before_end if value > 0)
    
    @property
    def outgo(self) -> float:
        # Расход для отображения обычно хотят видеть положительным
        return abs(sum(value for value in self._counts_before_end if value < 0))
    
    @property
    def end_count(self) -> float:
        # Расчет конечного остатка должен учитывать фактические значения (отрицательный расход)
        return self.start_count + sum(value for value in self._counts_before_end if value > 0) + sum(value for value in self._counts_before_end if value < 0)
    
    def add(self, trans: TransactionModel, start_date: datetime, end_date: datetime):
        vld.validate(trans, TransactionModel, "transaction")
        vld.validate(start_date, datetime, "start date")
        vld.validate(end_date, datetime, "end date")

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

        # !!! Убедитесь, что у TransactionModel есть атрибут 'count' (не 'quantity') !!!
        count = trans.quantity * coef 
        
        # !!! Убедитесь, что у TransactionModel есть атрибут 'datetime' (не 'date') !!!
        if trans.date < start_date:
            self._counts_before_start.append(count)
        elif start_date <= trans.date <= end_date:
            self._counts_before_end.append(count)
        else:
            pass # Транзакция проведена после конечной даты

    # --- НОВЫЕ МЕТОДЫ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ ВНУТРИ КЛАССА TBSLINE ---
    def to_display_data(self) -> Dict[str, Any]:
        """
        Возвращает данные строки ОСВ в виде словаря с русскими названиями
        и в порядке, удобном для отображения.
        """
        return {
            "Имя номенклатуры": self.nomenclature.name,
            "Единица измерения": self.measure_unit.name,
            "Начальный остаток": round(self.start_count, 3), # Округляем для вывода
            "Приход": round(self.income, 3),
            "Расход": round(self.outgo, 3),
            "Конечное количество": round(self.end_count, 3) # Имя изменено
        }

    @staticmethod
    def get_display_headers() -> List[str]:
        """
        Возвращает список заголовков столбцов в желаемом порядке для отображения.
        """
        return [
            "Имя номенклатуры",
            "Единица измерения",
            "Начальный остаток",
            "Приход",
            "Расход",
            "Конечное количество"
        ]