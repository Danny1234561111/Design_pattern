from typing import Optional, List, Self
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.dtos.recipe_dto import RecipeDto
from src.models.ingredient_model import IngredientModel
from src.singletons.repository import Repository


"""Модель рецепта"""
class RecipeModel(AbstractModel):
    # Наименование (наследуется от AbstractModel)

    # Описание рецепта (255, опционально)
    __description: Optional[str] = None

    # Количество порций, на которое расчитан рецепт
    __portions: Optional[int] = None

    # Время приготовления (в минутах)
    __cooking_time: Optional[int] = None

    # Список ингредиентов блюда
    __ingredients: List[IngredientModel] = list()

    # Текствовые шаги приготовления
    __steps: List[str] = list()

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        portions: Optional[int] = None,
        cooking_time: Optional[int] = None,
        ingredients: Optional[List[IngredientModel]] = None,
        steps: Optional[List[str]] = None
    ):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if portions is not None:
            self.portions = portions
        if cooking_time is not None:
            self.cooking_time = cooking_time
        if ingredients is not None:
            self.ingredients = ingredients
        if steps is not None:
            self.steps = steps
    
    """Поле текстового описания рецепта"""
    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter
    def description(self, value: Optional[str]):
        vld.is_str(value, "description", True, 255)
        self.__description = value
    
    """Поле порций рецепта"""
    @property
    def portions(self) -> int:
        return self.__portions
    
    @portions.setter
    def portions(self, value: int):
        vld.is_int(value, "portions")
        self.__portions = value
    
    """Поле времени готовки"""
    @property
    def cooking_time(self) -> int:
        return self.__cooking_time
    
    @cooking_time.setter
    def cooking_time(self, value: int):
        vld.is_int(value, "cooking_time")
        self.__cooking_time = value
    
    """Поле со списком ингредиентов рецепта"""
    @property
    def ingredients(self) -> List[IngredientModel]:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, value: List[IngredientModel]):
        vld.is_list_of(value, IngredientModel, "ingredients")
        self.__ingredients = value
    
    """Поле со списком текстовых шагов"""
    @property
    def steps(self) -> List[str]:
        return self.__steps
    
    @steps.setter
    def steps(self, value: List[str]):
        vld.is_list_of(value, str, "recipe steps")
        self.__steps = value

    """Фабричный метод из DTO"""
    def from_dto(dto: RecipeDto, repo: Repository) -> Self:
        ingredients = [
            IngredientModel.from_dto(ing_dto, repo)
            for ing_dto in dto.ingredients
        ]
        return RecipeModel(
            name=dto.name,
            description=dto.description,
            portions=dto.portions,
            cooking_time=dto.cooking_time,
            ingredients=ingredients,
            steps=dto.steps
        )
