import unittest
from src.models.measure_unit_model import MeasureUnitModel


class TestMeasureUnitModel(unittest.TestCase):

    # Инициализация новой базовой единицы измерения
    def test_measureunit_init_init_base_unit_fields_are_valid(self):
        # Подготовка
        c = 1
        name = "грамм"
        # Действие
        unit = MeasureUnitModel(c, name)
        # Проверка
        assert unit.coefficient == c
        assert unit.name == name
        assert unit.base_unit is None

    # Инициализация цепочки зависимых моделей единиц измерения
    def test_measureunit_init_units_with_base_units_fields_are_valid(self):
        # Подготовка
        c1, c2, c3 = 1, 1000, 1000
        name1, name2, name3 = "гр", "кг", "тонна"
        # Действие
        gramm = MeasureUnitModel(c1, name1)
        kilo = MeasureUnitModel(c2, name2, gramm)
        ton = MeasureUnitModel(c3, name3, kilo)
        # Проверка
        assert ton.coefficient == c3
        assert ton.base_unit.coefficient == c2
        assert ton.base_unit.base_unit.coefficient == c1
        assert ton.base_unit.base_unit.base_unit is None
        assert ton.base_unit.base_unit.name == kilo.base_unit.name


if __name__ == "__main__":
    unittest.main()
