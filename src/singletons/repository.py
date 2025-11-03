from typing import List, Any, Optional
from src.core.validator import Validator as vld
from src.core.exceptions import ParamException
from src.utils import get_properties


"""Репозиторий данных"""
class Repository:
    # Ссылка на объект Repository
    __instance = None

    # Словарь наименований моделей
    __data = dict()

    # Ключ для единиц измерения
    measure_unit_key: str = "measure_units"

    # Ключ для групп номенклатуры
    nomenclature_group_key: str = "nomenclature_groups"
    
    # Ключ для номенклатур
    nomenclatures_key: str = "nomenclatures"

    # Ключ для рецептов
    recipes_key: str = "recipes"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Словарь с объектами приложения"""
    @property
    def data(self) -> dict:
        return self.__data
    
    """Метод получения всех ключей Reposity по шаблону `*_key`"""
    @staticmethod
    def keys() -> List[str]:
        return [getattr(Repository, f) for f in get_properties(Repository)
                if f.endswith("_key")]
    
    """Инициализация списков в словаре данных"""    
    def initalize(self):
        # Все ключи будут ссылаться на словари формата name: object
        # с соответствующими объектами
        for key in Repository.keys():
            self.data[key] = dict()
    
    """Метод получения объекта в памяти по имени"""
    def get_by_name(self, name: str) -> Optional[Any]:
        vld.is_str(name, "item_name")
        for key in self.keys():
            items: dict = self.data[key]
            for _, item in items.items():
                if item.name.lower() == name.lower():
                    return item
        return None

    """Метод получения объекта в памяти по уникальному коду"""
    def get_by_unique_code(self, unique_code: str) -> Optional[Any]:
        vld.is_str(unique_code, "item_unique_code")
        for key in self.keys():
            items: list = self.data[key].values()
            items = [item
                     for item in items
                     if item.unique_code == unique_code]
            if len(items):
                return items[0]
        
        return None

    """Универсальный метод получения объекта в памяти"""
    def get(
        self,
        unique_code: Optional[str] = None,
        name: Optional[str] = None
    ) -> Optional[Any]:
        if unique_code is not None:
            return self.get_by_unique_code(unique_code)
        elif name is not None:
            return self.get_by_name(unique_code)
        else:
            raise ParamException(
                "Must be transmitted either unique_code, or name, "
                "but both is None"
            )
