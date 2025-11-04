from typing import List, Dict
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.logics.tbs_line import TbsLine
from src.models.storage_model import StorageModel
from src.models.transaction_model import TransactionModel
from src.singletons.repository import Repository
from src.singletons.start_service import StartService


"""Класс для расчёта оборотно-сальдовой ведомости"""
class OsdTbs:
    
    @staticmethod
    def calculate(
        storage: StorageModel, 
        start: date, 
        end: date,
        start_service: StartService
    ) -> List[TbsLine]:
        vld.validate(storage, StorageModel, "storage")
        vld.validate(start, date, "start date")
        vld.validate(end, date, "end date")

        start = datetime(start.year, start.month, start.day)
        end = datetime(end.year, end.month, end.day, 23, 59, 59)
        key = Repository.transactions_key
        
        
        items: List[TransactionModel] = list(
            start_service.data[key].values()
        )
        transactions = [item
                        for item in items
                        if (item.storage == storage and
                            item.date <= end)]


        
        data: Dict[str, TbsLine] = dict()
        for transaction in transactions:
            code = transaction.nomenclature.unique_code
            if code not in data:
                data[code] = TbsLine(transaction)
            line = data[code]
            line.add(transaction, start, end)
        
        return list(data.values())