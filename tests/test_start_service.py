import unittest
from src.singletons.start_service import StartService
from src.models.recipe_model import RecipeModel


class TestStartService(unittest.TestCase):
    # Путь до файла с тестовыми настройками
    __file_name: str = "tests/data/settings_models.json"

    # Объект сервиса
    __start_service: StartService = StartService()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start(self.__file_name)
    
    # Метод load() загружает 5 единиц измерения
    def test_startservice_load_load_units_added_5_units(self):
        # Подготовка
        count = len(self.__start_service.measure_units)
        # Проверка
        assert count == 5
    
    # Метод load() загружает единицу измерения 'килограмм',
    # базовая единица которого - это грамм из того же словаря
    def test_startservice_load_create_units_kilo_contains_gramm(self):
        # Подготовка
        gramm = self.__start_service.repository.get_by_name("грамм")
        kilo = self.__start_service.repository.get_by_name("килограмм")
        # Проверка
        assert kilo.base_unit == gramm
    
    # Повторный вызов метода start() не должен обновлять единицы измерения
    def test_startservice_start_run_method_again_measure_units_are_same(self):
        # Подготовка
        name1, name2 = "грамм", "килограмм"
        gramm1 = self.__start_service.repository.get_by_name(name1)
        kilo1 = self.__start_service.repository.get_by_name(name2)
        # Действие
        self.__start_service.start(self.__file_name)
        gramm2 = self.__start_service.repository.get_by_name(name1)
        kilo2 = self.__start_service.repository.get_by_name(name2)
        # Проверка
        assert gramm1 == gramm2
        assert kilo1 == kilo2
    
    # Повторный вызов метода start() не должен обновлять группы номенклатур
    def test_startservice_start_run_method_again_nomenclature_groups_are_same(self):
        # Подготовка
        name = "ингредиенты"
        unit = self.__start_service.repository.get_by_name(name)
        # Действие
        self.__start_service.start(self.__file_name)
        new_unit = self.__start_service.repository.get_by_name(name)
        # Проверка
        assert unit == new_unit
    
    # Метод load() загружает 5 номенклатур
    def test_startservice_load_load_nomeclatures_added_5_nomenclatures(self):
        # Подготовка
        count = len(self.__start_service.nomenclatures)
        # Проверка
        assert count == 5
    
    # Проверить рецепт омлета, загруженного из файла
    def test_startservice_load_check_omelette_recipe_all_fields_are_models(self):
        # Подготовка
        omelette = self.__start_service.repository.get_by_name("омлет")
        
        # Проверка
        assert isinstance(omelette, RecipeModel)
        for ingredient in omelette.ingredients:
            name = ingredient.nomenclature.name
            repo_nomenclature = self.__start_service.repository.get_by_name(name)
            assert repo_nomenclature == ingredient.nomenclature

            name = ingredient.measure_unit.name
            repo_unit = self.__start_service.repository.get_by_name(name)
            assert repo_unit == ingredient.measure_unit


if __name__ == "__main__":
    unittest.main()
