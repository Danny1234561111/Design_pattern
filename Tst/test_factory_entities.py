import unittest
from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
from Src.Core.validator import validator, operation_exception, argument_exception # Добавил import
from Src.Models.settings_model import settings_model
from unittest.mock import MagicMock
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import ResponseFormat  # Импортируем ResponseFormat
from Src.Models.company_model import company_model # Импортируем company_model

class TestFactoryEntities(unittest.TestCase):

    def setUp(self):
        # Создаем экземпляр company_model (пример, нужно адаптировать)
        company = company_model() # Замените на реальную инициализацию company_model

        # Создаем экземпляр settings_model и инициализируем его
        self.settings = settings_model(response_format=ResponseFormat.CSV, company=company)

        # Создаем экземпляр factory_entities и инициализируем его
        self.factory = factory_entities(self.settings)

    def test_create_csv_response(self):
        # Проверка создания объекта response_csv
        response = self.factory.create(ResponseFormat.CSV)
        self.assertIsInstance(response, response_csv)

    def test_create_markdown_response(self):
        # Проверка создания объекта response_md
        response = self.factory.create(ResponseFormat.MARKDOWN)
        self.assertIsInstance(response, response_md)

    def test_create_xml_response(self):
        # Проверка создания объекта response_xml
        response = self.factory.create(ResponseFormat.XML)
        self.assertIsInstance(response, response_xml)

    def test_create_json_response(self):
        # Проверка создания объекта response_json
        response = self.factory.create(ResponseFormat.JSON)
        self.assertIsInstance(response, response_json)

    def test_create_invalid_format_raises_exception(self):
        # Проверка, что при передаче неверного формата выбрасывается исключение
        with self.assertRaises(operation_exception):
            self.factory.create("invalid_format")

    def test_create_default_response(self):
        # Проверка создания объекта по умолчанию
        response = self.factory.create_default()
        self.assertIsInstance(response, response_csv)  # По умолчанию установлен формат csv

    def test_init_invalid_settings_raises_exception(self):
        # Проверка, что при передаче неверных настроек выбрасывается исключение
        invalid_settings = MagicMock()  # Создаем мок-объект для настроек
        with self.assertRaises(argument_exception):  # Ожидаем argument_exception
            self.factory = factory_entities(invalid_settings)  # Ошибка должна возникать при создании объекта

if __name__ == "__main__":
    unittest.main()