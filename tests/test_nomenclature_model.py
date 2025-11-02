import unittest
from src.core.exceptions import WrongTypeException, InvalidValueException
from src.models.nomenclature_model import NomenclatureModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel


class TestNomenclatureModel(unittest.TestCase):
    
    # Инициализация модели номенклатуры с валидными полями
    def test_nomenclaturemodel_init_valid_fields_no_exceptions(self):
        # Подготовка
        name = "Мука"
        group = NomenclatureGroupModel("сырьё")
        base_unit = MeasureUnitModel(1, "грамм")
        unit = MeasureUnitModel(1000, "кг", base_unit)

        # Действие
        nom = NomenclatureModel(name, group, unit)

        # Проверка
        assert nom.name == name
        assert nom.group == group
        assert nom.measure_unit == unit
    
    # Присваивание полю наименования невалидных значений
    def test_nomenclaturemodel_name_set_invalid_value_raises_exceptions(self):
        # Подготовка
        nom = NomenclatureModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            nom.name = 123
        with self.assertRaises(InvalidValueException):
            nom.name = ""
        with self.assertRaises(InvalidValueException):
            nom.name = 'a'*256

    # Присваивание полю группы номенклатуры невалидных значений
    def test_nomenclaturemodel_group_set_invalid_value_raises_exception(self):
        # Подготовка
        nom = NomenclatureModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            nom.group = 123

    # Присваивание полю группы единицы измерения невалидных значений
    def test_nomenclaturemodel_measureunit_set_invalid_value_raises_exception(self):
        # Подготовка
        nom = NomenclatureModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            nom.measure_unit = 123


if __name__ == "__main__":
    unittest.main()
