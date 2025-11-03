# src/models/stock_item_model.py
from typing import Dict, Any, Union
from datetime import date # Добавлено

class StockItem:
    def __init__(
        self,
        nomenclature: str,
        measure_unit: str, # Или MeasureUnitModel, если хотите ссылаться на объект
        initial_balance: Union[int, float] = 0.0,
        income: Union[int, float] = 0.0,
        expense: Union[int, float] = 0.0,
        final_balance: Union[int, float] = 0.0,
        # Если нужно, можно добавить даты для более точной симуляции
        # date: date = date.today() 
    ):
        self.nomenclature = nomenclature
        self.measure_unit = measure_unit
        self.initial_balance = float(initial_balance)
        self.income = float(income)
        self.expense = float(expense)
        self.final_balance = float(final_balance)
        # self.date = date

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект StockItem в словарь для JSON-сериализации."""
        return {
            "nomenclature": self.nomenclature,
            "measure_unit": self.measure_unit,
            "initial_balance": self.initial_balance,
            "income": self.income,
            "expense": self.expense,
            "final_balance": self.final_balance,
            # "date": self.date.isoformat() if hasattr(self, 'date') else None
        }