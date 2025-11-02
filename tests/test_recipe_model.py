import unittest
from src.models.recipe_model import RecipeModel


class TestRecipeModel(unittest.TestCase):

    # Присваивание полю description пустого значения
    def test_recipemodel_description_set_none_no_exceptions(self):
        # Подготовка
        recipe = RecipeModel()
        # Действие
        recipe.description = None
        # Проверка
        assert recipe.description is None
    
    # Присваивание полю description валидного значения
    def test_recipemodel_description_set_valid_value_no_exceptions(self):
        # Подготовка
        recipe = RecipeModel()
        description = "Рецепт омлета из 3 яиц"
        # Действие
        recipe.description = description
        # Проверка
        assert recipe.description == description


if __name__ == "__main__":
    unittest.main()
