import unittest
from src.core.exceptions import WrongTypeException
from src.logics.structure_converter import StructureConverter
from src.models.nomenclature_group_model import NomenclatureGroupModel


class TestStructureConverter(unittest.TestCase):

    # Экземпляр конвертера
    __converter: StructureConverter = StructureConverter()

    # Метод convert() возвращает тот же список из целых чисел
    def test_structureconverter_convert_list_of_ints_same_list(self):
        # Подготовка
        data = [1, 2, 3]
        # Действие
        result = self.__converter.convert(data)
        # Проверка
        assert result == data
    
    # Метод convert() возвращает список словарей с теми же значениями моделей
    # групп номенклатур
    def test_structureconverter_convert_list_of_models_valid_dict(self):
        # Подготовка
        data = [
            NomenclatureGroupModel("group1"),
            NomenclatureGroupModel("group2")
        ]
        expected_result = [
            {
                "unique_code": data[0].unique_code,
                "name": data[0].name,
            },
            {
                "unique_code": data[1].unique_code,
                "name": data[1].name,
            },
        ]
        # Действие
        result = self.__converter.convert(data)
        # Проверка
        assert result == expected_result
    
    # Метод convert() выкинет исключение при передачи неверного типа данных
    def test_structureconverter_convert_convert_not_structure_raise_wrongtype(self):
        # Проверка
        with self.assertRaises(WrongTypeException):
            self.__converter.convert(NomenclatureGroupModel("test"))
    
    # Метод convert() выкинет исключение при передачи списка данных
    # разного типа
    def test_structureconverter_convert_convert_list_of_different_types_raise_wrongtype(self):
        # Проверка
        with self.assertRaises(WrongTypeException):
            self.__converter.convert([True, 1, "str"])


if __name__ == "__main__":
    unittest.main()
