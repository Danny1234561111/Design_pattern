import unittest
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.logics.response_csv import ResponseCsv
from src.logics.response_markdown import ResponseMarkdown
from src.logics.response_json import ResponseJson
from src.logics.response_xml import ResponseXml
from src.logics.factory_entities import FactoryEntities


class TestFactoryEntities(unittest.TestCase):
    
    # Метод create() должен возвращать экземпляры ответов, соответствующих
    # типам ответов ResponseFormat
    def test_factoryentities_create_create_responses_using_response_format_no_exceptions(self):
        # Подготовка
        factory = FactoryEntities()
        formats_types = {
            ResponseFormat.CSV: ResponseCsv,
            ResponseFormat.MARKDOWN: ResponseMarkdown,
            ResponseFormat.JSON: ResponseJson,
            ResponseFormat.XML: ResponseXml,
        }
        # Действие и проверка
        for format, type_ in formats_types.items():
            response = factory.create(format)
            assert response is not None
            assert isinstance(response, type_)
            assert vld.is_superclass(AbstractResponse, response, "response")
    
    # Метод create() должен возвращать экземпляры ответов, соответствующих
    # строковым типам ответов
    def test_factoryentities_create_create_responses_using_strings_no_exceptions(self):
        # Подготовка
        factory = FactoryEntities()
        formats_types = {
            "csv": ResponseCsv,
            "markdown": ResponseMarkdown,
            "md": ResponseMarkdown,
            "json": ResponseJson,
            "xml": ResponseXml,
        }
        # Действие и проверка
        for format, type_ in formats_types.items():
            response = factory.create(format)
            assert response is not None
            assert isinstance(response, type_)
            assert vld.is_superclass(AbstractResponse, response, "response")
    
    # Метод create() выкидывает соответствующее исключение, если передан
    # несуществующий формат ответа
    def test_factoryentities_create_create_non_existent_response_raise_exception(self):
        # Подготовка
        factory = FactoryEntities()
        format = "html"
        # Действие и проверка
        with self.assertRaises(OperationException):
            factory.create(format)
    
    # Метод create_default() возвращает ответ того формата, который указан
    # в настройках
    def test_factoryentities_createdefault_create_default_response_no_exceptions(self):
        # Подготовка
        factory = FactoryEntities()
        # Действие
        response = factory.create_default()
        # Проверка
        assert response is not None
        assert isinstance(response, ResponseJson)


if __name__ == "__main__":
    unittest.main()
