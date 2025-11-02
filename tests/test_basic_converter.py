import unittest
from src.core.exceptions import WrongTypeException
from src.logics.basic_converter import BasicConverter


class TestBasicConverter(unittest.TestCase):

    # Экземпляр конвертера
    __converter: BasicConverter = BasicConverter()

    # Проверка на то, что метод convert() оставляет значения нетронутыми
    def test_basicconverter_convert_convert_primitive_types_returns_same(self):
        # Подготовка
        values = [True, 1, 2.0, "string", None]
        # Проверка
        for value in values:
            assert value == self.__converter.convert(value)
    
    # Метод convert() выкинет исключение при передачи неверного типа данных
    def test_basicconverter_convert_convert_not_primitive_type_raise_wrongtype(self):
        # Проверка
        with self.assertRaises(WrongTypeException):
            self.__converter.convert([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
