import json
from typing import Optional, Dict
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


"""Класс, наполняющий приложение эталлоными объектами разных типов"""
class StartService:
    # Ссылка на экземпляр StartService
    __instance = None

    # Путь до файла с загружаемыми объектами
    __file_name: str = ""

    # Ссылка на объект Repository
    __repository: Optional[Repository] = Repository()

    def __init__(self):
        self.__repository.initalize()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Поле пути до файла с загружаемыми объектами"""
    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = vld.is_file_exists(value)

    """Словарь данных репозитория"""
    @property
    def data(self) -> dict:
        return self.__repository.data
    
    """Объект репозитория"""
    @property
    def repository(self) -> Repository:
        return self.__repository

    """Группы номенклатур в репозитории"""
    @property
    def nomenclature_groups(self) -> Dict[str, NomenclatureGroupModel]:
        return self.data[Repository.nomenclature_group_key]
    
    """Единицы измерения в репозитории"""
    @property
    def measure_units(self) -> Dict[str, MeasureUnitModel]:
        return self.data[Repository.measure_unit_key]
    
    """Номенклатуры в репозитории"""
    @property
    def nomenclatures(self) -> Dict[str, NomenclatureModel]:
        return self.data[Repository.nomenclatures_key]
    @property
    def storages(self) -> Dict[str, StorageModel]:
        return self.data[Repository.storages_key]
    @property
    def transactions(self) -> Dict[str, TransactionModel]:
        return self.data[Repository.transactions_key]

    """Метод загрузки эталонных моделей и рецептов из файла настроек"""
    def load(self) -> bool:
        if not self.file_name:
            raise OperationException(
                f"Data can't be loaded, file_name field is empty"
            )
        with open(self.file_name, mode='r', encoding="utf-8") as file:
            objects = json.load(file)
            data = objects["models"]
            return self.convert(data)
    
    """Универсальный метод чтения и записи моделей из файла с помощью DTO
    
    Args:
        data (dict): общий словарь со всеми моделями
        data_key (str): ключ словаря data с целевыми моделями
        repo_key (str): ключ репозитория, который ссылается
            на словарь с моделями
        dto_type (type): класс, унаследованный от AbstractDto
        model_type (type): класс, унаследованный от AbstractModel
    """
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
            # Если объект с таким же именем уже существует, то пропускаем
            if self.__repository.get_by_name(item.get("name", "")):
                continue
            
            dto = dto_type().load(item)
            model = model_type.from_dto(dto, self.__repository)
            self.__repository.data[repo_key][model.name] = model

        return True
    
    """Метод конвертации объекта в модели групп номенклатур"""
    def __convert_nomenclature_groups(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenclature_groups",
            repo_key=Repository.nomenclature_group_key,
            dto_type=NomenclatureGroupDto,
            model_type=NomenclatureGroupModel
        )
    
    """Метод конвертации объекта в модели единиц измерения"""
    def __convert_measure_units(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="measure_units",
            repo_key=Repository.measure_unit_key,
            dto_type=MeasureUnitDto,
            model_type=MeasureUnitModel
        )
    
    """Метод конвертации объекта в модели номенклатур"""
    def __convert_nomenlatures(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenlatures",
            repo_key=Repository.nomenclatures_key,
            dto_type=NomenclatureDto,
            model_type=NomenclatureModel
        )

    """Метод конвертации объекта в модели рецептов"""
    def __convert_recipes(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="recipes",
            repo_key=Repository.recipes_key,
            dto_type=RecipeDto,
            model_type=RecipeModel
        )
        """Метод конвертации объекта в модели транзакций"""
    def __convert_transactions(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="transactions",
            repo_key=Repository.transactions_key, 
            dto_type=TransactionDto, 
            model_type=TransactionModel  
        )
    
    """Метод конвертации объекта в модели складов"""
    def __convert_storages(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="storages",
            repo_key=Repository.storages_key,
            dto_type=StorageDto,
            model_type=StorageModel 
        )
    """Метод конвертации объекта в модели"""
    def convert(self, data: dict) -> bool:
        vld.is_dict(data, "data")
        self.__convert_nomenclature_groups(data)
        self.__convert_measure_units(data)
        self.__convert_nomenlatures(data)
        self.__convert_recipes(data)
        
        self.__convert_storages(data) 
        self.__convert_transactions(data)  
    
    """Метод вызова методов генерации эталонных данных"""
    def start(self, file_name: str):
        self.file_name = file_name
        self.load()
