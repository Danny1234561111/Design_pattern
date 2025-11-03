from typing import List, Any, Optional, Dict
from src.core.validator import Validator as vld
from src.core.exceptions import ParamException
from datetime import date
from src.utils import get_properties  # Убедитесь, что этот импорт правильный
from src.models.stock_item_model import StockItem  # Импорт класса StockItem

"""Репозиторий данных"""
class Repository:
    # Ссылка на объект Repository
    __instance = None

    # Словарь наименований моделей
    __data = dict()

    # Ключи для данных в репозитории
    measure_unit_key: str = "measure_units"  # Ключ для единиц измерения
    nomenclature_group_key: str = "nomenclature_groups"  # Ключ для групп номенклатуры
    nomenclatures_key: str = "nomenclatures"  # Ключ для номенклатур
    recipes_key: str = "recipes"  # Ключ для рецептов

    # Новые ключи для складов и транзакций
    storages_key: str = "storages"  # Ключ для складов
    transactions_key: str = "transactions"  # Ключ для транзакций

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Словарь с объектами приложения"""
    @property
    def data(self) -> dict:
        return self.__data
    
    """Метод получения всех ключей в репозитории по шаблону `*_key`"""
    @staticmethod
    def keys() -> List[str]:
        return [getattr(Repository, f) for f in get_properties(Repository) if f.endswith("_key")]
    
    """Инициализация списков в словаре данных"""    
    def initalize(self):
        # Инициализация всех ключей
        for key in Repository.keys():
            self.data[key] = dict()
    
    """Метод получения объекта в памяти по имени"""
    def get_by_name(self, name: str) -> Optional[Any]:
        vld.is_str(name, "item_name")
        for key in self.keys():
            items: dict = self.data.get(key, {})  # Используем .get() для безопасности
            for _, item in items.items():
                if hasattr(item, 'name') and item.name.lower() == name.lower():  # Проверяем, что у объекта есть .name
                    return item
        return None

    """Метод получения объекта в памяти по уникальному коду"""
    def get_by_unique_code(self, unique_code: str) -> Optional[Any]:
        vld.is_str(unique_code, "item_unique_code")
        for key in self.keys():
            items: dict = self.data.get(key, {})  # Используем .get() для безопасности
            if unique_code in items:  # Если unique_code является ключом в словаре
                return items[unique_code]
            
            # Если unique_code не является ключом, но он есть внутри объекта
            for item in items.values():
                if hasattr(item, 'unique_code') and item.unique_code == unique_code:
                    return item
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
            return self.get_by_name(name)  # Исправлено: передаем name, а не unique_code
        else:
            raise ParamException(
                "Must be transmitted either unique_code, or name, "
                "but both are None"
            )

    def add_data(self, key: str, data_dict: Dict[str, Any]):
        """Добавляет или обновляет данные в репозитории по ключу."""
        vld.is_str(key, "data_key")
        vld.is_dict(data_dict, "data_dict")
        if key not in self.data:
            self.data[key] = {}
        self.data[key].update(data_dict)  # Обновляем существующий словарь

    # --- РЕАЛИЗАЦИЯ get_stock_data ---
    def get_stock_data(self, storage: str, start_date: date, end_date: date) -> List[StockItem]:
        """
        Получение оборотно-сальдовой ведомости (ОСВ) для заданного склада и периода.
        Эта реализация является МОКОВОЙ (т.е. симулированной)
        и возвращает статические данные.

        Args:
            storage (str): Имя склада.
            start_date (date): Дата начала периода.
            end_date (date): Дата окончания периода.

        Returns:
            List[StockItem]: Список объектов StockItem, представляющих ОСВ.
        """
        vld.is_str(storage, "storage name")
        vld.validate(start_date, date, "start_date")  # Если у вас есть валидация для date
        vld.validate(end_date, date, "end_date")  # Если у вас есть валидация для date

        # Здесь будет ваша реальная логика получения данных.
        # Для примера: генерируем моковые данные на основе номенклатуры
        
        # Получаем все номенклатуры из репозитория
        nomenclatures = self.data.get(self.nomenclatures_key, {}).values()
        measure_unit = self.data.get(self.measure_unit_key, {})  # Получаем словарь ед.измерения
        
        if not nomenclatures:
            return []

        stock_report: List[StockItem] = []

        # Пример очень упрощенной логики:
        # Для каждого наименования номенклатуры создаем StockItem
        for nom in nomenclatures:
            nomenclature_name = nom.name if hasattr(nom, 'name') else "Неизвестная номенклатура"
            
            # Получаем единицу измерения. Если nom.measure_unit является объектом,
            # то берем его имя. Иначе предполагаем, что это уже строка.
            measure_unit_name = "шт."
            if hasattr(nom, 'measure_unit') and nom.measure_unit:
                if hasattr(nom.measure_unit, 'name'):
                    measure_unit_name = nom.measure_unit.name
                elif isinstance(nom.measure_unit, str):
                    measure_unit_name = nom.measure_unit
            
            # Генерация условных (моковых) данных для остатков/приходов/расходов
            initial = float(hash(nomenclature_name + storage + str(start_date)) % 1000) / 10.0  # Случайное число
            income = float(hash(nomenclature_name + storage + str(end_date) + "inc") % 200) / 10.0
            expense = float(hash(nomenclature_name + storage + str(end_date) + "exp") % 150) / 10.0
            final = initial + income - expense

            stock_report.append(
                StockItem(
                    nomenclature=nomenclature_name,
                    measure_unit=measure_unit_name,  # Передаем имя единицы измерения
                    initial_balance=initial,
                    income=income,
                    expense=expense,
                    final_balance=final
                )
            )
        
        return stock_report