import unittest
from Src.Logics.response_md import response_md
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Core.common import common
from Src.Core.validator import operation_exception

class Testresponse_md(unittest.TestCase):

    # Проверка формирования MD из модели группы номенклатуры
    def test_response_md_create_create_md_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = response_md()
        entity = group_model.create("test")
        data = [entity]
        # Действие
        result = response.create("md", data)
        # Проверка
        self.assertIsNotNone(result)

        # Проверка соответствия формата MD (например, наличие заголовка)
        lines = result.strip().split("\n")
        self.assertTrue(lines[0].startswith("#"))  # Заголовок должен начинаться с #
        
        # Проверка соответствия полей
        props = common.get_fields(entity)
        for prop in props:
            self.assertIn(prop, result)

    # Проверка формирования MD из нескольких моделей единиц измерения
    def test_response_md_create_create_md_from_measureunit_models_not_none(self):
        # Подготовка
        response = response_md()
        data = [range_model.create("гр", 1), range_model.create("мл", 1)]
        # Действие
        result = response.create("md", data)
        # Проверка
        self.assertIsNotNone(result)

        # Проверка, что результат содержит все единицы измерения
        for unit in data:
            self.assertIn(unit.name, result)

    # Метод create() выбрасывает исключение при передаче списка из моделей разных типов
    def test_response_md_create_create_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = response_md()
        data = [range_model.create("гр", 1), group_model.create("группа")]
        # Действие и проверка
        with self.assertRaises(operation_exception):
            response.create("md", data)

if __name__ == "__main__":
    unittest.main()
