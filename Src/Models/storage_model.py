# Src/Models/storage_model.py
from Src.Core.validator import validator
from Src.Core.entity_model import entity_model
from typing import Dict
from Src.Models.nomenclature_model import nomenclature_model

"""
Модель склада
"""
class storage_model(entity_model):
    __address: str = ""
    __inventory: Dict[nomenclature_model, float] = {} #  Словарь: ингредиент -> количество

    """
    Адрес
    """
    @property
    def address(self) -> str:
        return self.__address.strip()

    @address.setter
    def address(self, value: str):
        validator.validate(value, str)
        self.__address = value.strip()

    """
    Инвентарь склада (ингредиенты и их количество)
    """
    @property
    def inventory(self) -> Dict[nomenclature_model, float]:
        return self.__inventory

    @inventory.setter
    def inventory(self, value: Dict[nomenclature_model, float]):
        # TODO: Валидация типов в словаре
        self.__inventory = value

    def add_item(self, item: nomenclature_model, quantity: float):
        """Добавляет ингредиент на склад"""
        if item in self.__inventory:
            self.__inventory[item] += quantity
        else:
            self.__inventory[item] = quantity

    def remove_item(self, item: nomenclature_model, quantity: float):
        """Удаляет ингредиент со склада"""
        if item in self.__inventory:
            if self.__inventory[item] >= quantity:
                self.__inventory[item] -= quantity
            else:
                raise ValueError("Недостаточно ингредиента на складе")
        else:
            raise ValueError("Ингредиент отсутствует на складе")