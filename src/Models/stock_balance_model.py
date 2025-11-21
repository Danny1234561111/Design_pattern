# models/stock_balance_model.py

from datetime import date

class StockBalanceModel:
    def __init__(self, storage_name: str, nomenclature_name: str, balance: float, date_calculated: date):
        self.storage_name = storage_name
        self.nomenclature_name = nomenclature_name
        self.balance = balance
        self.date_calculated = date_calculated