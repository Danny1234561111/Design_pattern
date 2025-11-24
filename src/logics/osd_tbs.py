from typing import List, Dict
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.logics.tbs_line import TbsLine
from src.logics.tbs_line_ost import TbsLineOst
from src.models.storage_model import StorageModel
from src.models.settings_model import SettingsModel
from src.models.transaction_model import TransactionModel
from src.models.ost_model import Ost
from src.models.nomenclature_model import NomenclatureModel
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.logics.prototype_report import PrototypeReport
from src.dtos.filter_dto import FiltredDto
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.core.filter_operators import filter_operators
class OsdTbs:

    @staticmethod
    def calculate(
        storage_id: str,
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
        filt.load({
            "field_name": "storage",
            "value": storage_id.name,
            "operator": filter_operators.like(),
        })
        
        filtered_transactions = prototype.filter(prototype, filt)

        if filters and filters.filters:
            for filter in filters.filters:
                filt = FiltredDto()
                filt.load(filter)
                filter["value"] = start_service.repository.get(unique_code=filter["value"])
                filtered_transactions = prototype.filter(filtered_transactions, filt)

        data: Dict[str, TbsLine] = {}

        for transaction in filtered_transactions.data:
            code = transaction.nomenclature.unique_code
            if code not in data:
                data[code] = TbsLine(transaction)
            line = data[code]
            line.add(transaction, start, end)

        all_nomenclatures = StartService().data[Repository.nomenclatures_key].keys()
        for key in all_nomenclatures:
            if key not in data:
                nomenclature = StartService().repository.get(unique_code=key)
                if nomenclature is None:
                    continue
                data[key] = TbsLine(Ost(
                    nomenclature=nomenclature,
                    quantity=0,  # Обнуляем счетчик
                    measure_unit=nomenclature.measure_unit
                ))
        tbs_lines: List[TbsLine] = list(data.values())
        headers = TbsLine.get_display_headers()
        display_data_rows = [line.to_display_data() for line in tbs_lines]
        
        return headers, display_data_rows
    @staticmethod
    def calculate_ost(
        block_date: date, 
        start_service: StartService,
    ) -> List[TbsLine]:
        vld.validate(block_date, date, "block date")
        
        block_date = datetime(block_date.year, block_date.month, block_date.day, 23, 59, 59)
        transactions = list(start_service.transactions.values())
        prototype = PrototypeReport(transactions)

        filt_block = FiltredDto()
        filt_next_info = FiltredDto()
        filt_block.load({
            "field_name": "date",
            "value": block_date,
            "operator": filter_operators.less(),
        })
        filt_next_info.load({
            "field_name": "date",
            "value": block_date,
            "operator": filter_operators.not_less(),
        })
        
        
        filtered_transactions = prototype.filter(prototype, filt_block)
        work_transactions = prototype.filter(prototype, filt_next_info)
        for i,tr in enumerate(work_transactions.data):
            work_transactions.data[i]= tr.name

        data: Dict[str, TbsLineOst] = {}

        for transaction in filtered_transactions.data:
            code = transaction.nomenclature.unique_code
            code_stor = transaction.storage.name
            if (code,code_stor) not in data:
                data[code,code_stor] = TbsLineOst(transaction)
            line = data[code,code_stor]
            line.add(transaction)

        tbs_lines: List[TbsLineOst] = list(data.values())
        headers = TbsLineOst.get_display_headers()
        display_data_rows = [line.to_display_data() for line in tbs_lines if line.quantity!=0]
        display_data_dict = [line.to_display_data() for line in tbs_lines if line.quantity!=0]
        return headers,display_data_rows,work_transactions.data,display_data_dict
    
    @staticmethod
    def calculate_new_ost(
        end_date:date,
        start_service: StartService,
    ) -> List[TbsLine]:
        # vld.validate(block_date, date, "block date")
        block_date: date = start_service.block_date
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        
        
        transactions = list(start_service.repository.next_transactions)
        for i,next in enumerate(transactions):
             transactions[i]= start_service.repository.get(name=next)
        prototype = PrototypeReport(transactions)

        filt = FiltredDto()
        filt1 = FiltredDto()
        filt.load({
            "field_name": "date",
            "value": end_date,
            "operator": filter_operators.less(),
        })
        filtered_transactions = prototype.filter(prototype, filt)

        data: Dict[str, TbsLineOst] = {}
        old_ost = start_service.repository.display_data_dict
        range = list(start_service.measure_units.values())
        for transaction in filtered_transactions.data:
            
            code = transaction.nomenclature.unique_code
            code_stor = transaction.storage.name
            if (code,code_stor) not in data:
                data[code,code_stor] = TbsLineOst(transaction)
            line = data[code,code_stor]
            line.add(transaction)
        
        for ost in old_ost:
            stor = start_service.repository.get(name=ost["Склад"])
            nomenclature = start_service.repository.get(name=ost["Имя номенклатуры"])
            transaction = TransactionModel(None,None,nomenclature,stor,ost["Остаток"],nomenclature.measure_unit,"transaction")
            code = nomenclature.unique_code
            code_stor = stor.name
            if (code,code_stor) not in data:
                data[code,code_stor] = TbsLineOst(transaction)
            line = data[code,code_stor]
            line.add(transaction)

        tbs_lines: List[TbsLineOst] = list(data.values())
        
        headers = TbsLineOst.get_display_headers()
        display_data_rows = [line.to_display_data() for line in tbs_lines if line.quantity!=0]
       

        
        

        return headers,display_data_rows
    