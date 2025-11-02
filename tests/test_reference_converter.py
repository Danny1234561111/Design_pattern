import unittest
from src.core.exceptions import WrongTypeException
from src.logics.reference_converter import ReferenceConverter
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel


class TestReferenceConverter(unittest.TestCase):

    # Экземпляр конвертера
    __converter: ReferenceConverter = ReferenceConverter()

    # Метод convert() конвертирует модель группы номенклатуры в словарь с
    # двумя ключами и теми же значенями
    def test_referenceconverter_convert_convert_nomenclature_group_valid_dict(self):
        # Подготовка
        name = "test"
        group = NomenclatureGroupModel(name)
        unique_code = group.unique_code
        expected_result = {
            "name": name,
            "unique_code": unique_code
        }
        # Действие
        result = self.__converter.convert(group)
        # Проверка
        assert result == expected_result
    
    # Метод convert() конвертирует модель группы номенклатуры в словарь с
    # двумя ключами и теми же значенями
    def test_referenceconverter_convert_convert_measure_unit_valid_dict(self):
        # Подготовка
        base_unit = MeasureUnitModel(1, "гр")
        unit = MeasureUnitModel(1000, "кг", base_unit)
        expected_result = {
            "unique_code": unit.unique_code,
            "coefficient": 1000.0,
            "name": unit.name,
            "base_unit": {
                "unique_code": base_unit.unique_code,
                "coefficient": 1.0,
                "name": base_unit.name,
                "base_unit": None
            }
        }
        # Действие
        result = self.__converter.convert(unit)
        # Проверка
        assert result == expected_result
    
    # Метод convert() выкинет исключение при передачи неверного типа данных
    def test_referenceconverter_convert_convert_not_abstractmodel_raise_wrongtype(self):
        # Проверка
        with self.assertRaises(WrongTypeException):
            self.__converter.convert([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
