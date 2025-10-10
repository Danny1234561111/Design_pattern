"""
Репозиторий данных
"""

from typing import Dict, List, Any

class reposity:
    __data: Dict[str, List[Any]] = {}

    DEFAULT_KEYS = {
        "range_model": [],
        "group_model": [],
        "nomenclature_model": [],
        "receipt_model": []
    }

    @property
    def data(self) -> Dict[str, List[Any]]:
        return self.__data

    """
    Ключ для единц измерений
    """
    @staticmethod
    def range_key() -> str:
        return "range_model"

    """
    Ключ для категорий
    """
    @staticmethod
    def group_key() -> str:
        return "group_model"

    """
    Ключ для номенклатуры
    """
    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature_model"

    """
    Ключ для рецептов
    """
    @staticmethod
    def receipt_key() -> str:
        return "receipt_model"

    """
    Инициализация
    """
    def initalize(self) -> None:
        self.__data = {key: [] for key in self.DEFAULT_KEYS}
