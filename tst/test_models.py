import unittest
import json

from src.models.company_models import (CompanyModel)
from src.settings_manager.settings_manager import SettingsManager

class TestModels(unittest.TestCase):  # Наследуемся от unittest.TestCase

    def test_empty_create_model_company_model(self):
        # Подготовка
        model = CompanyModel()
        # Действие
        # Проверка
        assert model.name == ""
    def test_notempty_create_model_company_model(self):
        # Подготовка
        model = CompanyModel()
        # Действие
        model.name = "test"

        # Проверка
        assert model.name!=""

    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "/Design_pattern/tst/settings.json"
        manager1 = SettingsManager(file_name)
        manager1.load()
        # Проверка
        assert manager1 != ""

    def test_load_createmodel_companymodel_equality(self):
        # Подготовка
        file_name = "/Design_pattern/tst/settings.json"
        manager1 = SettingsManager(file_name)
        manager2 = SettingsManager(file_name)
        manager1.load()
        manager1.load()
        # Проверка
        assert manager1 == manager2

    def test_load_settings_from_ocation(self):
        # Подготовка
        filepath = "/Design_pattern/tst/settings.json"
        manager = SettingsManager(filepath)
        manager.load()

        # Проверяем, что настройки загрузились правильно
        assert manager.settings.company.name=="Киви"
        assert manager.settings.company.inn== "111122223333"
        assert manager.settings.company.account== "40702810000"
        assert manager.settings.company.correspondent_account== "33301719999"
        assert manager.settings.company.bic== "123456111"
        assert manager.settings.company.type_of_ownership== "ООО"


    def test_check_company_fields(self):
        # Подготовка
        filename = "./Design_pattern/tst/settings.json"
        manager = SettingsManager(filename)
        manager.load()
        with self.assertRaises(ValueError):
            manager.settings.company.name = None

        manager.settings.company.name = "Киви"
        assert manager.settings.company.name == "Киви"

        with self.assertRaises(TypeError):
            manager.settings.company.inn = None

        with self.assertRaises(ValueError):
            manager.settings.company.inn = "111122233uu"
        with self.assertRaises(ValueError):
            manager.settings.company.inn = "11112223333894838943"

        manager.settings.company.inn = "123456789012"
        assert manager.settings.company.inn == "123456789012"

        manager.settings.company.inn = 111122223333
        assert manager.settings.company.inn == "111122223333"

        with self.assertRaises(TypeError):
            manager.settings.company.account = None

        with self.assertRaises(ValueError):
            manager.settings.company.account = "4070281000"

        manager.settings.company.account = "40702810000"
        assert manager.settings.company.account == "40702810000"

        manager.settings.company.account = 40702810000
        assert manager.settings.company.account == "40702810000"

        with self.assertRaises(TypeError):
            manager.settings.company.correspondent_account = None

        with self.assertRaises(ValueError):
            manager.settings.company.correspondent_account = "301"
        with self.assertRaises(ValueError):
            manager.settings.company.correspondent_account = "3330171bbbb"

        manager.settings.company.correspondent_account = "33301719999"
        assert manager.settings.company.correspondent_account == "33301719999"

        manager.settings.company.correspondent_account = 33301719999
        assert manager.settings.company.correspondent_account == "33301719999"

        with self.assertRaises(TypeError):
            manager.settings.company.bic = None

        with self.assertRaises(ValueError):
            manager.settings.company.bic = "2897893289723398732"
            with self.assertRaises(ValueError):
                manager.settings.company.bic = "12345611а"

        manager.settings.company.bic = "123456111"
        assert manager.settings.company.bic == "123456111"

        manager.settings.company.bic = 123456111
        assert manager.settings.company.bic == "123456111"

        with self.assertRaises(TypeError):
            manager.settings.company.type_of_ownership = None

        with self.assertRaises(ValueError):
            manager.settings.company.type_of_ownership = "000 компани"

        manager.settings.company.type_of_ownership = "ООО"
        assert manager.settings.company.type_of_ownership == "ООО"

if __name__ == '__main__':
    unittest.main()