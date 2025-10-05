
from typing import Optional, List, Dict
from Src.repository import Repository
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.recipe_model import RecipeModel
from Src.Models.storage_model import storage_model

class StartService:
    # Ссылка на экземпляр StartService
    __instance = None

    #
    __repository: Optional[Repository] = Repository()

    def __init__(self):
        self.__repository.data["measure_units"] = list()
        self.__repository.data["nomenclatures"] = list()
        self.__repository.data["groups"] = list()
        self.__repository.data["recipes"] = list()
        self.__repository.data["storages"] = list()

    @classmethod
    def new(cls):
        if cls.__instance is None:
            cls.__instance = StartService()
        return cls.__instance

    """Словарь данных репозитория"""

    @property
    def data(self) -> dict:
        return self.__repository.data

    """Метод генерации эталонных единиц измерения"""

    def __default_create_ranges(self):
        gramm = range_model.create_gramm()
        milliliter = range_model.create_milliliter() # Создаем миллилитры
        liter = range_model.create_liter(milliliter) # Создаем литры и связываем с миллилитром
        piece= range_model.create_piece()
        self.__repository.data["measure_units"].append(gramm)
        self.__repository.data["measure_units"].append(range_model.create_killogramm(gramm))
        self.__repository.data["measure_units"].append(milliliter) # Добавляем миллилитры
        self.__repository.data["measure_units"].append(liter)
        return gramm, milliliter, liter, piece

    def __create_default_nomenclatures(self, gramm: range_model, milliliter: range_model, liter: range_model,piece:range_model):  # Принимаем gramm, milliliter и liter
        # Создаем группы номенклатуры
        recipe_group = nomenclature_group_model()
        recipe_group.name = "Рецепты"
        self.__repository.data["groups"].append(recipe_group)

        # Создаем номенклатуру для рецепта 1 (Вафли)
        flour = nomenclature_model()
        flour.name = "Мука"
        flour.full_name = "Мука пшеничная высший сорт"
        flour.group = recipe_group
        flour.unit = gramm

        sugar = nomenclature_model()
        sugar.name = "Сахар"
        sugar.full_name = "Сахар-песок"
        sugar.group = recipe_group
        sugar.unit = gramm

        butter = nomenclature_model()
        butter.name = "Сливочное масло"
        butter.full_name = "Сливочное масло 82.5% жирности"
        butter.group = recipe_group
        butter.unit = gramm

        eggs = nomenclature_model()
        eggs.name = "Яйца"
        eggs.full_name = "Яйца куриные"
        eggs.group = recipe_group
        eggs.unit = piece

        vanillin = nomenclature_model()
        vanillin.name = "Ванилин"
        vanillin.full_name = "Ванилин (щепотка)"
        vanillin.group = recipe_group
        vanillin.unit = gramm

        # Создаем номенклатуру для рецепта 2 (Каша)
        oatmeal = nomenclature_model()
        oatmeal.name = "Овсяные хлопья"
        oatmeal.full_name = "Овсяные хлопья долгой варки"
        oatmeal.group = recipe_group
        oatmeal.unit = gramm

        milk = nomenclature_model()
        milk.name = "Молоко"
        milk.full_name = "Молоко 3.2% жирности"
        milk.group = recipe_group
        milk.unit = milliliter

        sugar_oat = nomenclature_model()
        sugar_oat.name = "Сахар"
        sugar_oat.full_name = "Сахар-песок"
        sugar_oat.group = recipe_group
        sugar_oat.unit = gramm

        butter_oat = nomenclature_model()
        butter_oat.name = "Сливочное масло"
        butter_oat.full_name = "Сливочное масло 82.5% жирности"
        butter_oat.group = recipe_group
        butter_oat.unit = gramm

        self.__repository.data["nomenclatures"].append(flour)
        self.__repository.data["nomenclatures"].append(sugar)
        self.__repository.data["nomenclatures"].append(butter)
        self.__repository.data["nomenclatures"].append(eggs)
        self.__repository.data["nomenclatures"].append(vanillin)
        self.__repository.data["nomenclatures"].append(oatmeal)
        self.__repository.data["nomenclatures"].append(milk)
        self.__repository.data["nomenclatures"].append(sugar_oat)
        self.__repository.data["nomenclatures"].append(butter_oat)

        return flour, sugar, butter, eggs, vanillin, oatmeal, milk, sugar_oat, butter_oat, recipe_group

    def __create_default_recipes(self, flour: nomenclature_model, sugar: nomenclature_model, butter: nomenclature_model, eggs: nomenclature_model, vanillin: nomenclature_model, oatmeal: nomenclature_model, milk: nomenclature_model, sugar_oat: nomenclature_model, butter_oat: nomenclature_model, recipe_group: nomenclature_group_model, gramm: range_model, milliliter: range_model,piece:range_model):
        # Рецепт 1 (Вафли)
        recipe1_ingredients: List[Dict[nomenclature_model, tuple[float, range_model]]] = [
            {flour: (100.0, gramm)},
            {sugar: (80.0, gramm)},
            {butter: (70.0, gramm)},
            {eggs: (1.0, piece)},
            {vanillin: (5.0, gramm)},
        ]

        recipe1 = RecipeModel(
            "Вафли хрустящие",
            recipe1_ingredients,
            "Смешать ингредиенты и выпекать в вафельнице.",
            recipe_group,
        )
        # Рецепт овсяной каши
        recipe2_ingredients: List[Dict[nomenclature_model, tuple[float, range_model]]] = [
            {oatmeal: (50.0, gramm)},
            {milk: (250.0, milliliter)},  # Используем миллилитры
            {sugar_oat: (15.0, gramm)},
            {butter_oat: (5.0, gramm)},
        ]

        recipe2 = RecipeModel(
            "Овсяная каша на молоке",
            recipe2_ingredients,
            "Сварить овсяную кашу на молоке, добавить сахар и масло.",
            recipe_group,
        )
        self.__repository.data["recipes"].append(recipe1)
        self.__repository.data["recipes"].append(recipe2)

    def __create_default_storages(self, flour, sugar, butter, eggs, vanillin, oatmeal, milk, sugar_oat, butter_oat):
        main_storage = storage_model()
        main_storage.name = "Основной склад"
        main_storage.address = "ул. ФБКИ, д. 1" #

        # Заполняем склад начальными запасами
        main_storage.add_item(flour, 1000.0)  # 1000 грамм муки
        main_storage.add_item(sugar, 500.0)  # 500 грамм сахара
        main_storage.add_item(butter, 300.0) # 300 грамм масла
        main_storage.add_item(eggs, 12.0)   # 12 штук яиц
        main_storage.add_item(vanillin, 50.0) # 50 грамм ванилина
        main_storage.add_item(oatmeal, 1500) # 1500 грамм овсянки
        main_storage.add_item(milk, 5000) # 5 литров молока (5000 мл)
        main_storage.add_item(sugar_oat, 400) # 400 грамм сахара
        main_storage.add_item(butter_oat, 200) # 200 грамм масла

        self.__repository.data["storages"].append(main_storage)


    """Метод вызова методов генерации дефолтных данных"""

    def start(self):
        gramm, milliliter, liter,piece = self.__default_create_ranges() # Получаем gramm и milliliter
        flour, sugar, butter, eggs, vanillin, oatmeal, milk, sugar_oat, butter_oat, recipe_group = self.__create_default_nomenclatures(gramm, milliliter, liter,piece)
        self.__create_default_storages(flour, sugar, butter, eggs, vanillin, oatmeal, milk, sugar_oat, butter_oat)
        self.__create_default_recipes(flour, sugar, butter, eggs, vanillin, oatmeal, milk, sugar_oat, butter_oat, recipe_group, gramm, milliliter,piece)
