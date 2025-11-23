import json
from typing import Optional, Dict
from datetime import date
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.dtos.measure_unit_dto import MeasureUnitDto
from src.dtos.nomenclature_dto import NomenclatureDto
from src.dtos.nomenclature_group_dto import NomenclatureGroupDto
from src.dtos.recipe_dto import RecipeDto
from src.models.recipe_model import RecipeModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.transaction_model import TransactionModel
from src.dtos.transaction_dto import TransactionDto
from src.dtos.storage_dto import StorageDto
from src.models.storage_model import StorageModel
from src.singletons.repository import Repository
import datetime


class StartService:
    __instance = None
    __file_name: str = ""
    __repository: Optional[Repository] = Repository()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = vld.is_file_exists(value)

    @property
    def data(self) -> dict:
        return self.__repository.data
    @property
    def block_date(self) -> date:
        return self.__repository.block_date
    
    @block_date.setter
    def block_date(self,value:date) -> date:
        self.__repository.block_date=value
    
    @property
    def repository(self) -> Repository:
        return self.__repository

    @property
    def nomenclature_groups(self) -> Dict[str, NomenclatureGroupModel]:
        return self.data[Repository.nomenclature_group_key]
    
    @property
    def measure_units(self) -> Dict[str, MeasureUnitModel]:
        return self.data[Repository.measure_unit_key]
    
    @property
    def nomenclatures(self) -> Dict[str, NomenclatureModel]:
        return self.data[Repository.nomenclatures_key]
    @property
    def storages(self) -> Dict[str, StorageModel]:
        return self.data[Repository.storages_key]
    @property
    def transactions(self) -> Dict[str, TransactionModel]:
        return self.data[Repository.transactions_key]
    @property
    def ost(self) -> date:
        return self.objects[Repository.ost_key]

    def load(self) -> bool:
        self.__repository.initalize()
        if not self.file_name:
            raise OperationException(
                f"Data can't be loaded, file_name field is empty"
            )
        try:
            with open(self.file_name, mode='r', encoding="utf-8") as file:
                objects = json.load(file)
                data = objects["models"]
                block=None
                if "block_date" in objects:
                    block=datetime.datetime.strptime(objects["block_date"],"%Y-%m-%d").date()
                return self.convert(data,block)
        except json.JSONDecodeError as e:
            raise OperationException(f"Invalid JSON file: {e}")
    
    def __get_ost_file_name(self) -> str:
        """Генерирует имя файла для остатков на основе основного файла"""
        base_name = self.file_name.replace('.json', '')
        return f"{base_name}_ost.json"
    
    def save_repository_data(self):
        """Сохраняет данные репозитория в отдельный файл для остатков"""
        ost_file_name = self.__get_ost_file_name()
        
        repository_data = self.__get_repository_data()
        
        # Сериализуем данные безопасно
        def default_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            return str(obj)
        
        try:
            with open(ost_file_name, mode='w', encoding="utf-8") as file:
                json.dump(repository_data, file, ensure_ascii=False, indent=2, default=default_serializer)
        except Exception as e:
            raise OperationException(f"Failed to save repository data: {e}")

    def load_repository_data(self) -> bool:
        """Загружает данные репозитория из файла остатков"""
        ost_file_name = self.__get_ost_file_name()
        
        try:
            with open(ost_file_name, mode='r', encoding="utf-8") as file:
                repo_data = json.load(file)
                self.__load_repository_data(repo_data)
                return True
        except FileNotFoundError:
            return False
        except json.JSONDecodeError as e:
            raise OperationException(f"Invalid OST JSON file: {e}")

    def __get_repository_data(self) -> dict:
        return {
            "headers": self.repository.headers,
            "turnovers_history": self.repository.turnovers_history,
            "next_transactions": [str(txn) for txn in self.repository.next_transactions],
            "display_data_dict": self.repository.display_data_dict,
            "block_date": self.repository.block_date.isoformat() if self.repository.block_date else None
        }

    def __load_repository_data(self, repo_data: dict):
        if "headers" in repo_data:
            self.repository.headers = repo_data["headers"]
        if "turnovers_history" in repo_data:
            self.repository.turnovers_history = repo_data["turnovers_history"]
        if "next_transactions" in repo_data:
            self.repository.next_transactions = repo_data["next_transactions"]
        if "display_data_dict" in repo_data:
            self.repository.display_data_dict = repo_data["display_data_dict"]
        if "block_date" in repo_data and repo_data["block_date"]:
            self.repository.block_date = datetime.datetime.strptime(
                repo_data["block_date"], "%Y-%m-%d"
            ).date()

    def __convert_models(
        self,
        data: dict,
        data_key: str,
        repo_key: str,
        dto_type: type,
        model_type: type,
    ) -> bool:
        vld.is_dict(data, "data")
        vld.is_str(data_key, "data_key")
        vld.is_str(repo_key, "repo_key")

        items = data.get(data_key, [])
        if not items:
            return False
        
        for item in items:
            if self.__repository.get_by_name(item.get("name", "")):
                continue
            
            dto = dto_type().load(item)
            model = model_type.from_dto(dto, self.__repository)
            self.__repository.data[repo_key][model.name] = model

        return True
    
    def __convert_nomenclature_groups(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenclature_groups",
            repo_key=Repository.nomenclature_group_key,
            dto_type=NomenclatureGroupDto,
            model_type=NomenclatureGroupModel
        )
    
    def __convert_measure_units(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="measure_units",
            repo_key=Repository.measure_unit_key,
            dto_type=MeasureUnitDto,
            model_type=MeasureUnitModel
        )
    
    def __convert_nomenlatures(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenlatures",
            repo_key=Repository.nomenclatures_key,
            dto_type=NomenclatureDto,
            model_type=NomenclatureModel
        )

    def __convert_recipes(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="recipes",
            repo_key=Repository.recipes_key,
            dto_type=RecipeDto,
            model_type=RecipeModel
        )
    def __convert_transactions(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="transactions",
            repo_key=Repository.transactions_key, 
            dto_type=TransactionDto, 
            model_type=TransactionModel  
        )
    def convert_ost(self, block_date:date = None) -> bool:
        if block_date is None:
            # Пытаемся загрузить из файла остатков
            if self.load_repository_data():
                return True
            else:
                raise OperationException(
                    "Block date is not specified and no saved OST data found"
                )
        
        # Проверяем, совпадает ли block_date с сохраненным
        if (self.repository.block_date and 
            self.repository.block_date == block_date and
            self.repository.headers and 
            self.repository.turnovers_history):
            return True
        
        # Вычисляем новые данные
        from src.logics.osd_tbs import OsdTbs
        headers,display_data_rows,work_transactions,display_data_dict = OsdTbs.calculate_ost(block_date,self)
        self.repository.headers = headers
        self.repository.turnovers_history = display_data_rows
        self.repository.next_transactions = work_transactions
        self.repository.display_data_dict= display_data_dict
        self.repository.block_date = block_date
        self.save_repository_data()
        return True

        
    
    def __convert_storages(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="storages",
            repo_key=Repository.storages_key,
            dto_type=StorageDto,
            model_type=StorageModel 
        )
    def convert(self, data: dict,block_date) -> bool:
        
        vld.is_dict(data, "data")
        
        self.__convert_nomenclature_groups(data)
        self.__convert_measure_units(data)
        self.__convert_nomenlatures(data)
        self.__convert_recipes(data)
        
        self.__convert_storages(data) 
        self.__convert_transactions(data)
        if block_date:
            self.__repository.block_date = block_date
            self.convert_ost(block_date)
    
    def start(self, file_name: str):
        self.file_name = file_name
        self.load()