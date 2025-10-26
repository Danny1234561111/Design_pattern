import unittest
from unittest.mock import patch, mock_open
import json
import os
from Src.start_service import start_service
from Src.Core.validator import argument_exception, operation_exception

class TestStartService(unittest.TestCase):

    def setUp(self):
        self.service = start_service()
        self.test_dir = os.path.dirname(__file__)
        self.test_config_path = os.path.join(self.test_dir, 'test_config.json')
        self.empty_test_config_path = os.path.join(self.test_dir, 'empty_test_config.json')
        self.create_test_files()

    def create_test_files(self):
        # Создание тестового файла с корректными данными
        test_data = {
            "company": {
                "name": "Рога и копыта",
                "inn": 123456789
            },
            "default_receipt": {
                "group_model": [{"name": "Group1"}, {"name": "Group2"}],
                "range_model": [{"name": "Unit1"}, {"name": "Unit2"}],
                "nomenclature_model": [{"name": "Product1"}, {"name": "Product2"}],
                "receipt_model": [{"name": "Receipt1"}, {"name": "Receipt2"}]
            }
        }
        
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        with open(self.empty_test_config_path, 'w', encoding='utf-8'):
            pass  # Создаем пустой файл

    @patch('builtins.open', new_callable=mock_open, read_data='{"company": {}, "default_receipt": {}}')
    def test_load_empty_company_section(self, mock_file):
        # Проверяем исключение, если секция "company" пуста
        self.service.file_name = self.test_config_path
        with self.assertRaises(operation_exception) as context:
            self.service.load()
        self.assertIn("Ошибка при загрузке данных компании.", str(context.exception))

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "company": {
            "name": "Рога и копыта",
            "inn": 123456789
        },
        "default_receipt": {
            "group_model": [{"name": "Group1"}, {"name": "Group2"}],
            "range_model": [{"name": "Unit1"}, {"name": "Unit2"}],
            "nomenclature_model": [{"name": "Product1"}, {"name": "Product2"}],
            "receipt_model": [{"name": "Receipt1"}, {"name": "Receipt2"}]
        }
    }))
    def test_load_data_success(self, mock_file):
        # Проверяем успешную загрузку данных
        self.service.file_name = self.test_config_path
        result = self.service.load()
        self.assertTrue(result)
        self.assertIn("group_model", self.service._reposity.data)
        self.assertIn("range_model", self.service._reposity.data)
        self.assertIn("nomenclature_model", self.service._reposity.data)

    def test_load_file_not_found(self):
        # Проверяем исключение при попытке загрузить несуществующий файл
        self.service.file_name = 'non_existent_file.json'
        with self.assertRaises(argument_exception) as context:
            self.service.load()
        self.assertIn("Файл \"non_existent_file.json\" не найден.", str(context.exception))

    def test_load_empty_file(self):
        # Проверяем исключение при загрузке пустого файла
        self.service.file_name = self.empty_test_config_path
        with self.assertRaises(operation_exception) as context:
            self.service.load()
        self.assertIn("Файл конфигурации пуст.", str(context.exception))

    def test_load_file_not_found(self):
    # Проверяем исключение при попытке установить несуществующий файл
        with self.assertRaises(argument_exception) as context:
            self.service.file_name = 'non_existent_file.json'
        self.assertIn("Файл \"non_existent_file.json\" не найден.", str(context.exception))

if __name__ == '__main__':
    unittest.main()