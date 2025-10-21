import unittest
from Src.Logics.response_json import response_json
from Src.Models.group_model import group_model
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import ResponseFormat
from Src.Core.validator import validator
from Src.Core.abstract_response import abstract_response
from Src.Core.entity_model import entity_model
from Src.Core.validator import argument_exception
from Src.Core.exceptions import ParamException, WrongTypeException
from Src.Models.range_model import range_model
from Src.Core.common import common
from Src.Core.validator import operation_exception
import json

class Testresponse_json(unittest.TestCase):

    # Проверка формирования JSON из модели группы номенклатуры
    def test_response_json_create_create_json_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = response_json()
        entity = group_model.create("test")
        data = [entity]
        # Действие
        result = response.create("json", data)
        # Проверка
        self.assertIsNotNone(result)

        # Проверка, что результат является корректным JSON
        json_data = json.loads(result)
        self.assertIsInstance(json_data, list)
        self.assertEqual(len(json_data), 1)

        # Проверка соответствия полей
        props = common.get_fields(entity)
        for field in props:
            self.assertIn(field, json_data[0])

    # Проверка формирования JSON из нескольких моделей единиц измерения
    def test_response_json_create_create_json_from_measureunit_models_not_none(self):
        # Подготовка
        response = response_json()
        data = [range_model.create("гр", 1), range_model.create("мл", 1)]
        # Действие
        result = response.create("json", data)
        # Проверка
        self.assertIsNotNone(result)

        # Проверка, что результат является корректным JSON
        json_data = json.loads(result)
        self.assertIsInstance(json_data, list)
        self.assertEqual(len(json_data), len(data))

    # Метод create() выбрасывает исключение при передаче списка из моделей разных типов
    def test_response_json_create_create_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = response_json()
        data = [range_model.create("гр", 1), group_model.create("группа")]
        # Действие и проверка
        with self.assertRaises(operation_exception):
            response.create("json", data)

if __name__ == "__main__":
    unittest.main()
