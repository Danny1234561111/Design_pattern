from typing import List, Dict
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.logics.tbs_line import TbsLine
from src.models.storage_model import StorageModel
from src.models.transaction_model import TransactionModel
from src.models.nomenclature_model import NomenclatureModel
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.logics.prototype_report import PrototypeReport
from src.dtos.filter_dto import FiltredDto
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.core.filter_operators import filter_operators
"""Класс для расчёта оборотно-сальдовой ведомости"""
class OsdTbs:
    
    @staticmethod
    def calculate(
        storage_id:str,
        start: date, 
        end: date,
        start_service: StartService,
        filters: filter_sorting_dto = None,

    ) -> List[TbsLine]:
        vld.validate(storage_id, str, "storage_id")
        vld.validate(start, date, "start date")
        vld.validate(end, date, "end date")
        
        start = datetime(start.year, start.month, start.day)
        end = datetime(end.year, end.month, end.day, 23, 59, 59)
        transactions = list(start_service.transactions.values())
        prototype = PrototypeReport(transactions)
        filt = FiltredDto()
        storage = start_service.repository.get(unique_code=storage_id)
        data={
            "field_name": "storage",
            "value": storage_id,
            "operator": filter_operators.like(),
            }
        filt.load(data)
        filtered_transactions = prototype.filter(prototype,filt)
        if (filters.filters):
            for filter in filters.filters:
                
                filt = FiltredDto()
                filt.load(filter)
                filter["value"]= start_service.repository.get(unique_code=filter["value"])
                filtered_transactions = prototype.filter(filtered_transactions,filt)

        data: Dict[str, TbsLine] = dict()
        for transaction in filtered_transactions.data:
            code = transaction.nomenclature.unique_code
            if code not in data:
                data[code] = TbsLine(transaction)
                line = data[code]
                line.add(transaction, start, end)

        tbs_keys = data.keys()
        all_keys = StartService().data[Repository.nomenclatures_key].keys()
        other_keys = set(all_keys) - set(tbs_keys)
        
        for key in other_keys:
            nomenclature = StartService().repository.get(unique_code=key)
            if nomenclature is None:
                continue
            data[key] = TbsLine(TransactionModel(
                nomenclature=nomenclature,
                storage=storage,
                count=0,
                measure_unit=nomenclature.measure_unit
            ))
        tbs_lines: TbsLine = list(data.values())
        
        headers = TbsLine.get_display_headers()
        display_data_rows = [line.to_display_data() for line in tbs_lines]
        
        return headers,display_data_rows