
import unittest
import uuid

# Adjust import paths if necessary
from Src.settings_manager import settings_manager
from Src.Models.company_model import company_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Core.abstract_model import abstact_model

# Internal exception classes
class ArgumentException(ValueError):
    pass

class OperationException(Exception):
    pass

class ErrorProxy:  # Added error proxy
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TestModels(unittest.TestCase):

    """
    Проверить создание основной модели
    Данные после создания должны быть пустыми
    """
    # def test_empty_createmodel_companymodel(self):
    #     # Подготовка
    #     model = company_model()
    #
    #     # Действие
    #
    #     # Проверки
    #     self.assertEqual(model.name, "")

    """
    Проверить создание основной модели
    Данные меняем. Данные должны быть
    """
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = company_model(name="")

        # Действие
        model.name = "test"

        # Проверки
        self.assertEqual(model.name, "test")
        self.assertNotEqual(model.name, "")

    """
    Проверить создание основной модели
    Данные загружаем через json настройки
    """
    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "settings.json"
        manager = settings_manager()
        manager.file_name = file_name

        # Действие
        try:
            manager.load()
            result = True
        except Exception:
            result = False

        # Проверки
        self.assertTrue(result)
        print(manager.file_name)

    """
    Проверить создание основной модели
    Данные загружаем. Проверяем работу Singletone
    """
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = "./settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()

        # Действие
        manager1.load()

        self.assertEqual(manager1.settings, manager2.settings)


    """
    Проверка на сравнение двух по значению одинаковых моделей
    """

    def text_equals_storage_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = storage_model()
        storage1.id = id
        storage2 = storage_model()
        storage2.id = id
        # Действие GUID

        # Проверки
        assert storage1 == storage2

    def test_range_model_creation(self):
        base_range = range_model("грамм", 1.0)
        self.assertEqual(base_range.name, "грамм")
        self.assertEqual(base_range.conversion_factor, 1.0)
        # self.assertIsNone(base_range.base)

        new_range = range_model("кг", 1000.0, base_range)
        self.assertEqual(new_range.name, "кг")
        self.assertEqual(new_range.conversion_factor, 1000.0)
        self.assertEqual(new_range.base, base_range)
        self.assertEqual(new_range.base.name, base_range.name)
        self.assertEqual(new_range.base.name, "грамм")

    def test_range_model_invalid_conversion_factor(self):
        with self.assertRaises(ValueError) as context:
            range_model("something", -1.0) # Changed to direct call, ValueError expected
        self.assertIn("Коэффициент пересчета должен быть больше 0", str(context.exception))


    def test_nomenclature_model_creation(self):

        group = nomenclature_group_model("Test Group")
        unit = range_model("kg", 1.0)


        nomenclature = nomenclature_model(
            name="Test Item",
            full_name="Test Item Full Name",
            group=group,
            unit=unit,
        )


        self.assertEqual(nomenclature.name, "Test Item")
        self.assertEqual(nomenclature.full_name, "Test Item Full Name")
        self.assertEqual(nomenclature.group.name, "Test Group")
        self.assertEqual(nomenclature.unit.name, "kg")

    def test_nomenclature_group_model_creation(self):
        group = nomenclature_group_model("Test Group")

        self.assertEqual(group.name, "Test Group")

    def test_storage_model_creation(self):
        storage = storage_model(name="Test Storage")
        storage.id = uuid.uuid4().hex


        self.assertEqual(storage.name, "Test Storage")
        self.assertIsNotNone(storage.id)
    # def abstact(self):
    #     a=abstact_model()
    #     assert a==a

if __name__ == '__main__':
    unittest.main()
