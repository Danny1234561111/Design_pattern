
from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.receipt_dto import receipt_dto
from Src.Dtos.Ingredient_dto import IngredientDto
import json
from typing import Optional, Dict


"""
TODO
1. Учитывать возможность изменения порядка методов создания данных
(либо кидать соответствующее исключение)

"""
"""Класс, наполняющий приложение эталлоными объектами разных типов"""
class start_service:
    # Ссылка на экземпляр StartService
    __instance = None

    # Путь до файла с загружаемыми объектами
    __file_name: str = ""

    # Ссылка на объект reposity
    __reposity: Optional[reposity] = reposity()

    def __init__(self):
        self.__reposity.initalize()

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
        self.__file_name = validator.is_file_exists(value)

    """Словарь данных репозитория"""
    @property
    def data(self) -> dict:
        return self.__reposity.data
    
    """Объект репозитория"""
    @property
    def reposity(self) -> reposity:
        return self.__reposity

    """Группы номенклатур в репозитории"""
    @property
    def nomenclature_groups(self) -> Dict[str, group_model]:
        return self.data[reposity.group_key]
    
    """Единицы измерения в репозитории"""
    @property
    def measure_units(self) -> Dict[str, range_model]:
        return self.data[reposity.range_key]
    
    """Номенклатуры в репозитории"""
    @property
    def nomenclatures(self) -> Dict[str, nomenclature_model]:
        return self.data[reposity.nomenclature_key]

    """Метод загрузки эталонных моделей и рецептов из файла настроек"""
    def load(self) -> bool:
        if not self.file_name:
            raise operation_exception(
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
        validator.is_dict(data, "data")
        validator.is_str(data_key, "data_key")
        validator.is_str(repo_key, "repo_key")

        items = data.get(data_key, [])
        if not items:
            return False
        
        for item in items:
            # Если объект с таким же именем уже существует, то пропускаем
            if self.__reposity.get(item.get("name", "")):
                continue
            
            dto = dto_type().load(item)
            model = model_type.from_dto(dto, self.__reposity)
            self.__reposity.data[repo_key][model.name] = model

        return True
    
    """Метод конвертации объекта в модели групп номенклатур"""
    def __convert_nomenclature_groups(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenclature_groups",
            repo_key=reposity.nomenclature_group_key,
            dto_type=dto,
            model_type=group_model
        )
    
    """Метод конвертации объекта в модели единиц измерения"""
    def __convert_measure_units(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="measure_units",
            repo_key=reposity.measure_unit_key,
            dto_type=receipt_dto,
            model_type=range_model
        )
    
    """Метод конвертации объекта в модели номенклатур"""
    def __convert_nomenlatures(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenlatures",
            repo_key=reposity.nomenclature_key,
            dto_type=nomenclature_dto,
            model_type=nomenclature_model
        )

    """Метод конвертации объекта в модели рецептов"""
    def __convert_recipes(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="recipes",
            repo_key=reposity.recipes_key,
            dto_type=receipt_dto,
            model_type=receipt_model
        )
    
    """Метод конвертации объекта в модели"""
    def convert(self, data: dict) -> bool:
        validator.is_dict(data, "data")
        self.__convert_nomenclature_groups(data)
        self.__convert_measure_units(data)
        self.__convert_nomenlatures(data)
        self.__convert_recipes(data)
    
    """Метод вызова методов генерации эталонных данных"""
    def start(self, file_name: str):
        self.file_name = file_name
        self.load()