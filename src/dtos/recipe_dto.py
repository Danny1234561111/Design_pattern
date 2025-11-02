from typing import List, Optional, Self, Union
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto
from src.dtos.Ingredient_dto import IngredientDto


"""DTO для модели IngredientModel"""
class RecipeDto(AbstractDto):
    # Описание рецепта (255, опционально)
    __description: Optional[str]

    # Количество порций, на которое расчитан рецепт
    __portions: Optional[int]

    # Время приготовления (в минутах)
    __cooking_time: Optional[int]

    # Список ингредиентов блюда
    __ingredients: Union[List[dict], List[IngredientDto]] = list()

    # Текствовые шаги приготовления
    __steps: List[str] = list()

    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        super().load(data)
        for i, ingredient in enumerate(self.ingredients):
            self.ingredients[i] = IngredientDto().load(ingredient)
        
        return self
    
    """Описание рецепта"""
    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter
    def description(self, value: Optional[str]):
        vld.is_str(value, "description", True, 255)
        self.__description = value
    
    """Порции рецепта"""
    @property
    def portions(self) -> int:
        return self.__portions
    
    @portions.setter
    def portions(self, value: int):
        vld.is_int(value, "portions")
        self.__portions = value
    
    """Время готовки"""
    @property
    def cooking_time(self) -> int:
        return self.__cooking_time
    
    @cooking_time.setter
    def cooking_time(self, value: int):
        vld.is_int(value, "cooking_time")
        self.__cooking_time = value
    
    """Список ингредиентов рецепта"""
    @property
    def ingredients(self) -> Union[List[dict], List[IngredientDto]]:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, value: Union[List[dict], List[IngredientDto]]):
        vld.is_list_of(value, (dict, IngredientDto), "ingredients")
        self.__ingredients = value
    
    """Список текстовых шагов"""
    @property
    def steps(self) -> List[str]:
        return self.__steps
    
    @steps.setter
    def steps(self, value: List[str]):
        vld.is_list_of(value, str, "ingredient steps")
        self.__steps = value
