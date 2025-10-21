import unittest
from Src.Logics.response_csv import response_csv
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

class Testresponse_csv(unittest.TestCase):

    # Проверка формирования CSV из модели группы номенклатуры
    def test_response_csv_create_create_csv_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = response_csv()
        entity = group_model.create("test")
        data = [entity]
        # Действие
        result = response.create("csv", data)
        # Проверка
        self.assertIsNotNone(result)

        rows = result.split("\n")
        head = rows[0]
        props = common.get_fields(entity)
        props_head = response_csv.delimitter.join(props)
        self.assertEqual(head, props_head)
    
    # Проверка формирования CSV из нескольких моделей единиц измерения
    def test_response_csv_create_create_csv_from_measureunit_models_not_none(self):
        # Подготовка
        response = response_csv()
        data = [range_model.create("гр", 1), range_model.create("мл", 1)]
        # Действие
        result = response.create("csv", data)
        # Проверка
        self.assertIsNotNone(result)
        
        rows = result.split("\n")
        self.assertEqual(len(rows), len(data) + 2)
    

    # Метод create() выбрасывает исключение при передаче списка из моделей разных типов
    def test_response_csv_create_create_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = response_csv()
        data = [range_model.create("гр", 1), group_model.create("группа")]
        # Действие и проверка
        with self.assertRaises(operation_exception):
            response.create("csv", data)

if __name__ == "__main__":
    unittest.main()
