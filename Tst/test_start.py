
# Tst/test_start.py
import unittest
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.start_service import StartService
from Src.repository import Repository
from Src.Models.storage_model import storage_model


class TestStart(unittest.TestCase):
    __start_service = StartService.new() # Получаем экземпляр StartService через фабричный метод

    def setUp(self):
        # Инициализируем репозиторий перед каждым тестом
        self.__start_service = StartService.new()
        self.__start_service.start()
        self.repository = Repository() # Получаем экземпляр Repository


    def test_start_service_start_unit_not_empty(self):
        # Проверка, что единицы измерения созданы
        self.assertGreater(len(self.repository.data["measure_units"]), 0)

    def test_start_service_start_nomenclature_not_empty(self):
        # Проверка, что номенклатура создана
        self.assertGreater(len(self.repository.data["nomenclatures"]), 0)

    def test_start_service_start_groups_not_empty(self):
        # Проверка, что группы созданы
        self.assertGreater(len(self.repository.data["groups"]), 0)

    def test_start_service_start_recipes_not_empty(self):
        # Проверка, что рецепты созданы
        self.assertEqual(len(self.repository.data["recipes"]), 2)  # Проверяем, что создано 2 рецепта

    def test_nomenclature_has_group_and_unit(self):
        nomenclatures = self.repository.data["nomenclatures"]
        self.assertGreater(len(nomenclatures), 0)
        for nom in nomenclatures:
            self.assertTrue(isinstance(nom, nomenclature_model))
            self.assertTrue(isinstance(nom.group, nomenclature_group_model))
            self.assertTrue(isinstance(nom.unit, range_model))

    def test_milliliter_created(self):
        measure_units = self.repository.data["measure_units"]
        milliliter_exists = False
        for unit in measure_units:
            if unit.name == "миллилитр":
                milliliter_exists = True
                break
        self.assertTrue(milliliter_exists)

    def test_recipes_created(self):
        recipes = self.repository.data["recipes"]
        recipe_names = [recipe.name for recipe in recipes]
        self.assertIn("Вафли хрустящие", recipe_names)  # Изменено название
        self.assertIn("Овсяная каша на молоке", recipe_names)

    def test_storage_has_inventory(self):
        storages = self.repository.data["storages"]
        self.assertGreater(len(storages), 0)
        for storage in storages:
            self.assertTrue(isinstance(storage, storage_model))
            self.assertGreater(len(storage.inventory), 0)  # Проверяем, что инвентарь не пустой

    def test_storage_inventory_contains_items(self):
        storages = self.repository.data["storages"]
        self.assertGreater(len(storages), 0)
        for storage in storages:
            self.assertTrue(isinstance(storage, storage_model))
            inventory = storage.inventory
            self.assertGreater(len(inventory), 0)

            # Проверяем наличие нескольких ингредиентов на складе
            self.assertTrue(any(item.name == "Мука" and quantity > 0 for item, quantity in inventory.items()))
            self.assertTrue(any(item.name == "Сахар" and quantity > 0 for item, quantity in inventory.items()))
            self.assertTrue(any(item.name == "Сливочное масло" and quantity > 0 for item, quantity in inventory.items()))
            self.assertTrue(any(item.name == "Яйца" and quantity > 0 for item, quantity in inventory.items()))
            self.assertTrue(any(item.name == "Ванилин" and quantity > 0 for item, quantity in inventory.items()))
            self.assertTrue(any(item.name == "Овсяные хлопья" and quantity > 0 for item, quantity in inventory.items()))
            self.assertTrue(any(item.name == "Молоко" and quantity > 0 for item, quantity in inventory.items()))

    def test_waffles_recipe_has_correct_ingredients(self):
        recipes = self.repository.data["recipes"]
        waffles_recipe = next((r for r in recipes if r.name == "Вафли хрустящие"), None)
        self.assertIsNotNone(waffles_recipe, "Рецепт вафель не найден")

        # Проверяем, что ингредиенты связаны с правильной номенклатурой и единицами измерения
        ingredients = waffles_recipe.ingredients
        self.assertEqual(len(ingredients), 5, "Неверное количество ингредиентов в рецепте вафель")

        # Проверяем муку
        flour_ingredient = next((i for i in ingredients if list(i.keys())[0].name == "Мука"), None)
        self.assertIsNotNone(flour_ingredient, "Ингредиент 'Мука' не найден")
        flour_nom = list(flour_ingredient.keys())[0]
        flour_qty, flour_unit = list(flour_ingredient.values())[0]
        self.assertEqual(flour_qty, 100.0, "Неверное количество муки")
        self.assertEqual(flour_unit.name, "грамм", "Неверная единица измерения для муки")
        self.assertEqual(flour_nom.name, "Мука")

        # Проверяем сахар
        sugar_ingredient = next((i for i in ingredients if list(i.keys())[0].name == "Сахар"), None)
        self.assertIsNotNone(sugar_ingredient, "Ингредиент 'Сахар' не найден")
        sugar_nom = list(sugar_ingredient.keys())[0]
        sugar_qty, sugar_unit = list(sugar_ingredient.values())[0]
        self.assertEqual(sugar_qty, 80.0, "Неверное количество сахара")
        self.assertEqual(sugar_unit.name, "грамм", "Неверная единица измерения для сахара")
        self.assertEqual(sugar_nom.name, "Сахар")

        # Проверяем сливочное масло
        butter_ingredient = next((i for i in ingredients if list(i.keys())[0].name == "Сливочное масло"), None)
        self.assertIsNotNone(butter_ingredient, "Ингредиент 'Сливочное масло' не найден")
        butter_nom = list(butter_ingredient.keys())[0]
        butter_qty, butter_unit = list(butter_ingredient.values())[0]
        self.assertEqual(butter_qty, 70.0, "Неверное количество сливочного масла")
        self.assertEqual(butter_unit.name, "грамм", "Неверная единица измерения для сливочного масла")
        self.assertEqual(butter_nom.name, "Сливочное масло")

        # Проверяем яйца
        eggs_ingredient = next((i for i in ingredients if list(i.keys())[0].name == "Яйца"), None)
        self.assertIsNotNone(eggs_ingredient, "Ингредиент 'Яйца' не найден")
        eggs_nom = list(eggs_ingredient.keys())[0]
        eggs_qty, eggs_unit = list(eggs_ingredient.values())[0]
        self.assertEqual(eggs_qty, 1.0, "Неверное количество яиц")
        #TODO Тут нужно создать проверку единиц измерения
        self.assertEqual(eggs_nom.name, "Яйца")

        vanillin_ingredient = next((i for i in ingredients if list(i.keys())[0].name == "Ванилин"), None)
        self.assertIsNotNone(vanillin_ingredient, "Ингредиент 'Ванилин' не найден")
        vanillin_nom = list(vanillin_ingredient.keys())[0]
        vanillin_qty, vanillin_unit = list(vanillin_ingredient.values())[0]
        self.assertEqual(vanillin_qty, 5.0, "Неверное количество ванилина")
        self.assertEqual(vanillin_unit.name, "грамм", "Неверная единица измерения для ванилина")
        self.assertEqual(vanillin_nom.name, "Ванилин")

