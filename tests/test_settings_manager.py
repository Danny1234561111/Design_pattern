import unittest
from src.core.response_format import ResponseFormat
from src.singletons.settings_manager import SettingsManager


class TestSettingsManager(unittest.TestCase):

    # Заполнение наименования и вида собственности компании
    # значениями по умолчанию при инициализации менеджера настроек
    def test_settingsmanager_init_no_load_company_with_default_fields(self):
        # Подготовка
        manager = SettingsManager()
        # Проверка
        assert manager.settings.company.name == "Default Name"
        assert manager.settings.company.ownership == "owner"

    # Проверка на синглтон SettingsManager
    def test_settingsmanager_new_two_instances_settings_and_companies_are_same(self):
        # Подготовка
        manager1 = SettingsManager()
        manager2 = SettingsManager()
        # Проверка
        assert manager1.settings == manager2.settings
        assert manager1.settings.company == manager2.settings.company
    
    # Загрузка существующего валидного файла настроек
    def test_settingsmanager_load_load_valid_file_returns_true(self):
        # Подготовка
        manager = SettingsManager()
        # Проверка
        assert manager.load("data/settings.json")
    
    # Загрузка данных компании из settings.json
    def test_settingsmanager_load_load_valid_file_fields_are_valid(self):
        # Подготовка
        manager = SettingsManager()
        # Действие
        manager.load("data/settings.json")
        # Проверка
        assert manager.settings.company.name == "Danny MAD Entertainment"
        assert manager.settings.company.inn == 385693061393
        assert manager.settings.company.account == 34583289581
        assert manager.settings.company.corr_account == 95847306800
        assert manager.settings.company.bic == 458205943
        assert manager.settings.company.ownership == "owner"
        assert manager.settings.response_format == ResponseFormat.JSON
    
    # Загрузка данных компании из файла в другой директории
    def test_settingsmanager_load_load_other_valid_file_fields_are_valid(self):
        # Подготовка
        manager = SettingsManager()
        # Действие
        manager.load("tests/data/settings_valid.json")
        # Проверка
        assert manager.settings.company.name == "Test Company"
        assert manager.settings.company.inn == 123456789123
        assert manager.settings.company.account == 12345678912
        assert manager.settings.company.corr_account == 12345678912
        assert manager.settings.company.bic == 123456789
        assert manager.settings.company.ownership == "owner"
        assert manager.settings.response_format == ResponseFormat.CSV
    
    # Загрузка валидного файла без полей corr_account и bic
    def test_settingsmanager_load_load_valid_file_without_few_fields_no_exceptions(self):
        # Подготовка
        manager = SettingsManager()
        # Действие
        manager.load("tests/data/settings_without_few_fields.json")
        # Проверка
        assert manager.settings.company.name == "Test Company"
        assert manager.settings.company.inn == 123456789123
        assert manager.settings.company.account == 12345678912
        assert manager.settings.company.corr_account == None
        assert manager.settings.company.bic == None
        assert manager.settings.company.ownership == "owner"
    
    # Загрузка валидного файла с дополнительными полями
    def test_settingsmanager_load_load_valid_file_with_extra_fields_no_exceptions(self):
        # Подготовка
        manager = SettingsManager()
        # Действие
        manager.load("tests/data/settings_with_extra_fields.json")
        # Проверка
        assert manager.settings.company.name == "Test Company"
        assert manager.settings.company.inn == 123456789123
        assert manager.settings.company.account == 12345678912
        assert manager.settings.company.corr_account == 12345678912
        assert manager.settings.company.bic == 123456789
        assert manager.settings.company.ownership == "owner"
        assert getattr(manager.settings.company, "year", 2000)
        assert getattr(manager.settings.company,
                       "extra_field", "some value")
    
    # Загрузка данных компании из невалидного файла
    def test_settingsmanager_load_load_invalid_file_returns_false(self):
        # Подготовка
        manager = SettingsManager()
        # Проверка
        assert not manager.load("tests/data/settings_invalid.json")
    
    # Загрузка данных компании из несуществующего файла
    def test_settingsmanager_load_load_not_exists_file_file_not_found(self):
        # Подготовка
        manager = SettingsManager()
        # Проверка
        with self.assertRaises(FileNotFoundError):
            manager.load("data/settings_not_exists.json")


if __name__ == "__main__":
    unittest.main()
