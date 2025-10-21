import unittest
from Src.Logics.response_xml import response_xml
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Core.common import common
from Src.Core.validator import operation_exception

class Testresponse_xml(unittest.TestCase):

    # Проверка формирования XML из модели группы номенклатуры
    def test_response_xml_create_create_xml_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = response_xml()
        entity = group_model.create("test")
        data = [entity]
        # Действие
        result = response.create("xml", data)
        # Проверка
        self.assertIsNotNone(result)

        # Проверка, что результат является корректным XML
        self.assertTrue(result.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn('<root>', result)
        self.assertIn('</root>', result)

        # Проверка соответствия полей
        props = common.get_fields(entity)
        for prop in props:
            self.assertIn(f'<{prop}>', result)
            self.assertIn(f'</{prop}>', result)

    # Проверка формирования XML из нескольких моделей единиц измерения
    def test_response_xml_create_create_xml_from_measureunit_models_not_none(self):
        # Подготовка
        response = response_xml()
        data = [range_model.create("гр", 1), range_model.create("мл", 1)]
        # Действие
        result = response.create("xml", data)
        # Проверка
        self.assertIsNotNone(result)

        # Проверка, что результат является корректным XML
        self.assertTrue(result.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        # Метод create() выбрасывает исключение при передаче списка из моделей разных типов
    def test_response_xml_create_create_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = response_xml()
        data = [range_model.create("гр", 1), group_model.create("группа")]
        # Действие и проверка
        with self.assertRaises(operation_exception):
            response.create("xml", data)

if __name__ == "__main__":
    unittest.main()

