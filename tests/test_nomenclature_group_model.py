import unittest
from src.core.exceptions import InvalidValueException
from src.models.nomenclature_group_model import NomenclatureGroupModel


class TestNomenclatureGroupModel(unittest.TestCase):
    
    # Инициализация модели группы номенклатуры без параметров
    def test_nomenclaturegroup_init_empty_constructor_name_not_set(self):
        # Подготовка
        group = NomenclatureGroupModel()
        # Проверка
        assert group.name == ""

    # Инициализация модели группы номенклатуры с валиным именем
    def test_nomenclaturegroup_init_set_valid_name_no_exceptions(self):
        # Подготовка
        name = "товар"
        group = NomenclatureGroupModel(name)
        # Проверка
        assert group.name == name

    # Инициализация модели группы номенклатуры с слишком длинным именем
    def test_nomenclaturegroup_init_set_long_name_raises_invalid_value(self):
        # Проверка
        with self.assertRaises(InvalidValueException):
            NomenclatureGroupModel('a'*51)


if __name__ == "__main__":
    unittest.main()
