import unittest
from datetime import datetime
from src.core.exceptions import ParamException
from src.dtos.recipe_dto import RecipeDto
from src.logics.factory_converters import FactoryConverters
from src.logics.basic_converter import BasicConverter
from src.logics.datetime_converter import DatetimeConverter
from src.logics.reference_converter import ReferenceConverter
from src.logics.structure_converter import StructureConverter
from src.models.measure_unit_model import MeasureUnitModel


class TestFactoryConverters(unittest.TestCase):

    # Экземпляр фабрики
    __factory: FactoryConverters = FactoryConverters()
    
    # При передаче в метод create() целого числа возвращается BasicConverter
    def test_factoryconverters_create_create_from_int_returns_basicconverter(self):
        # Подготовка
        value = 1
        # Действие
        result = self.__factory.create(value)
        # Проверка
        assert isinstance(result, BasicConverter)
    
    # При передаче в метод create() None возвращается BasicConverter
    def test_factoryconverters_create_create_from_none_returns_basicconverter(self):
        # Подготовка
        value = None
        # Действие
        result = self.__factory.create(value)
        # Проверка
        assert isinstance(result, BasicConverter)
    
    # При передаче в метод create() datetime возвращается BasicConverter
    def test_factoryconverters_create_create_from_datetime_returns_basicconverter(self):
        # Подготовка
        value = datetime(2000, 1, 1)
        # Действие
        result = self.__factory.create(value)
        # Проверка
        assert isinstance(result, DatetimeConverter)
    
    # При передаче в метод create() MeasureUnitModel возвращается BasicConverter
    def test_factoryconverters_create_create_from_measure_unit_returns_basicconverter(self):
        # Подготовка
        value = MeasureUnitModel(1, "гр")
        # Действие
        result = self.__factory.create(value)
        # Проверка
        assert isinstance(result, ReferenceConverter)
    
    # При передаче в метод create() списка возвращается BasicConverter
    def test_factoryconverters_create_create_from_list_returns_basicconverter(self):
        # Подготовка
        value = list()
        # Действие
        result = self.__factory.create(value)
        # Проверка
        assert isinstance(result, StructureConverter)
    
    # При передаче в метод create() значения с необрабатываемым значением
    # выкидывается исключение
    def test_factoryconverters_create_create_from_recipe_dto_returns_basicconverter(self):
        # Подготовка
        value = RecipeDto()
        # Проверка
        with self.assertRaises(ParamException):
            self.__factory.create(value)


if __name__ == "__main__":
    unittest.main()
