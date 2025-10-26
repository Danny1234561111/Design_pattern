import unittest
from Src.Logics.factory_entities import factory_entities
from Src.Logics.response_csv import response_csv
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
from Src.Core.validator import operation_exception
from Src.Core.response_format import ResponseFormat

class TestFactoryEntities(unittest.TestCase):

    def test_create_with_valid_format_string_csv(self):
        response_object = factory_entities.create("CSV")
        self.assertIsInstance(response_object, response_csv)

    def test_create_with_valid_format_string_markdown(self):
        response_object = factory_entities.create("MARKDOWN")
        self.assertIsInstance(response_object, response_md)

    def test_create_with_valid_format_string_xml(self):
        response_object = factory_entities.create("XML")
        self.assertIsInstance(response_object, response_xml)

    def test_create_with_valid_format_string_json(self):
        response_object = factory_entities.create("JSON")
        self.assertIsInstance(response_object, response_json)

    def test_create_with_valid_format_enum_csv(self):
        response_object = factory_entities.create(ResponseFormat.CSV)
        self.assertIsInstance(response_object, response_csv)

    def test_create_with_valid_format_enum_markdown(self):
        response_object = factory_entities.create(ResponseFormat.MARKDOWN)
        self.assertIsInstance(response_object, response_md)

    def test_create_with_valid_format_enum_xml(self):
        response_object = factory_entities.create(ResponseFormat.XML)
        self.assertIsInstance(response_object, response_xml)

    def test_create_with_valid_format_enum_json(self):
        response_object = factory_entities.create(ResponseFormat.JSON)
        self.assertIsInstance(response_object, response_json)

    def test_create_with_invalid_format_string(self):
        with self.assertRaises(operation_exception) as cm:
            factory_entities.create("invalid_format_string")
        self.assertEqual(str(cm.exception), "Формат не верный")

if __name__ == '__main__':
    unittest.main()