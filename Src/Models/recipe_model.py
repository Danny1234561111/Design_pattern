from typing import List, Dict, Tuple
from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model


class RecipeModel(entity_model):
    __ingredients: List[Dict[nomenclature_model, Tuple[float, range_model]]]
    __instructions: str
    __group: nomenclature_group_model

    def __init__(self, name:str, ingredients: List[Dict[nomenclature_model, Tuple[float, range_model]]], instructions: str, group: nomenclature_group_model):
        self.name=name
        self.ingredients = ingredients
        self.instructions = instructions
        self.group = group

    @property
    def ingredients(self) -> List[Dict[nomenclature_model, Tuple[float, range_model]]]:
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: List[Dict[nomenclature_model, Tuple[float, range_model]]]):
        # TODO: validator for list
        self.__ingredients = value

    @property
    def instructions(self) -> str:
        return self.__instructions

    @instructions.setter
    def instructions(self, value: str):
        validator.validate(value, str)
        self.__instructions = value

    @property
    def group(self) -> nomenclature_group_model:
        return self.__group

    @group.setter
    def group(self, value: nomenclature_group_model):
        self.__group = value
