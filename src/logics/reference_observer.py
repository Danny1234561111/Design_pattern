from abc import ABC, abstractmethod
from typing import Dict, Any
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.singletons.repository import Repository
from src.singletons.start_service import StartService

class ReferenceObserver(ABC):
    """Абстрактный класс наблюдателя для справочников"""
    
    @abstractmethod
    def on_before_delete(self, reference_type: str, name: str) -> bool:
        """Вызывается перед удалением элемента"""
        pass
    
    @abstractmethod
    def on_after_update(self, reference_type: str, name: str, data: Dict[str, Any]):
        """Вызывается после обновления элемента"""
        pass

class UsageCheckObserver(ReferenceObserver):
    """Наблюдатель для проверки использования элементов"""
    
    def __init__(self):
        self.repository = Repository()
        self.start_service = StartService()
    
    def on_before_delete(self, reference_type: str, name: str) -> bool:
        """Проверяет использование элемента перед удалением"""
        
        if reference_type == "nomenclatures":
            return self._check_nomenclature_usage(name)
        elif reference_type == "measure_units":
            return self._check_measure_unit_usage(name)
        elif reference_type == "nomenclature_groups":
            return self._check_group_usage(name)
        elif reference_type == "storages":
            return self._check_storage_usage(name)
        
        return True
    
    def on_after_update(self, reference_type: str, name: str, data: Dict[str, Any]):
        """Обрабатывает изменения после обновления элемента"""
        if reference_type == "nomenclatures":
            self._update_nomenclature_references(name, data)
        elif reference_type == "measure_units":
            self._update_measure_unit_references(name, data)
    
    def _check_nomenclature_usage(self, name: str) -> bool:
        """Проверяет использование номенклатуры в рецептах и транзакциях"""
        # Проверка в рецептах
        recipes = self.repository.data.get(Repository.recipes_key, {})
        for recipe_name, recipe in recipes.items():
            if hasattr(recipe, 'ingredients'):
                for ingredient in recipe.ingredients:
                    if hasattr(ingredient, 'nomenclature') and getattr(ingredient.nomenclature, 'name', None) == name:
                        raise OperationException(
                            f"Номенклатура '{name}' используется в рецепте '{recipe_name}'"
                        )
        
        # Проверка в транзакциях
        transactions = self.repository.data.get(Repository.transactions_key, {})
        for txn_name, txn in transactions.items():
            if hasattr(txn, 'nomenclature_name') and txn.nomenclature_name == name:
                raise OperationException(
                    f"Номенклатура '{name}' используется в транзакции '{txn_name}'"
                )
        
        # Проверка в остатках
        if hasattr(self.start_service.repository, 'turnovers_history'):
            for item in self.start_service.repository.turnovers_history:
                if item.get("Имя номенклатуры") == name:
                    raise OperationException(
                        f"Номенклатура '{name}' используется в остатках"
                    )
        
        return True
    
    def _check_measure_unit_usage(self, name: str) -> bool:
        """Проверяет использование единицы измерения"""
        # Проверка в номенклатурах
        nomenclatures = self.repository.data.get(Repository.nomenclatures_key, {})
        for nom_name, nom in nomenclatures.items():
            if hasattr(nom, 'measure_unit') and getattr(nom.measure_unit, 'name', None) == name:
                raise OperationException(
                    f"Единица измерения '{name}' используется в номенклатуре '{nom_name}'"
                )
        
        # Проверка в рецептах
        recipes = self.repository.data.get(Repository.recipes_key, {})
        for recipe_name, recipe in recipes.items():
            if hasattr(recipe, 'ingredients'):
                for ingredient in recipe.ingredients:
                    if hasattr(ingredient, 'measure_unit') and getattr(ingredient.measure_unit, 'name', None) == name:
                        raise OperationException(
                            f"Единица измерения '{name}' используется в рецепте '{recipe_name}'"
                        )
        
        return True
    
    def _check_group_usage(self, name: str) -> bool:
        """Проверяет использование группы номенклатуры"""
        nomenclatures = self.repository.data.get(Repository.nomenclatures_key, {})
        for nom_name, nom in nomenclatures.items():
            if hasattr(nom, 'group') and getattr(nom.group, 'name', None) == name:
                raise OperationException(
                    f"Группа номенклатуры '{name}' используется в номенклатуре '{nom_name}'"
                )
        
        return True
    
    def _check_storage_usage(self, name: str) -> bool:
        """Проверяет использование склада"""
        transactions = self.repository.data.get(Repository.transactions_key, {})
        for txn_name, txn in transactions.items():
            if hasattr(txn, 'storage_name') and txn.storage_name == name:
                raise OperationException(
                    f"Склад '{name}' используется в транзакции '{txn_name}'"
                )
        
        return True
    
    def _update_nomenclature_references(self, name: str, data: Dict[str, Any]):
        """Обновляет ссылки на номенклатуру при её изменении"""
        # Обновление в рецептах
        if 'name' in data:
            new_name = data['name']
            recipes = self.repository.data.get(Repository.recipes_key, {})
            for recipe_name, recipe in recipes.items():
                if hasattr(recipe, 'ingredients'):
                    for ingredient in recipe.ingredients:
                        if hasattr(ingredient, 'nomenclature') and getattr(ingredient.nomenclature, 'name', None) == name:
                            ingredient.nomenclature = new_name
    
    def _update_measure_unit_references(self, name: str, data: Dict[str, Any]):
        """Обновляет ссылки на единицу измерения при её изменении"""
        if 'name' in data:
            new_name = data['name']
            nomenclatures = self.repository.data.get(Repository.nomenclatures_key, {})
            for nom_name, nom in nomenclatures.items():
                if hasattr(nom, 'measure_unit') and getattr(nom.measure_unit, 'name', None) == name:
                    nom.measure_unit = new_name

class RecalculationObserver(ReferenceObserver):
    """Наблюдатель для пересчета остатков при изменениях"""
    
    def __init__(self):
        self.start_service = StartService()
    
    def on_before_delete(self, reference_type: str, name: str) -> bool:
        return True
    
    def on_after_update(self, reference_type: str, name: str, data: Dict[str, Any]):
        """Пересчитывает остатки после изменений"""
        if reference_type in ["nomenclatures", "measure_units"]:
            self._recalculate_balances()
    
    def _recalculate_balances(self):
        """Пересчитывает остатки по дате блокировки"""
        if self.start_service.repository.block_date:
            self.start_service.convert_ost(self.start_service.repository.block_date)
