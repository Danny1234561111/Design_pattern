import unittest
import datetime
from src.core.exceptions import WrongTypeException
from src.logics.datetime_converter import DatetimeConverter


class TestDatetimeConverter(unittest.TestCase):

    # Экземпляр конвертера
    __converter: DatetimeConverter = DatetimeConverter()

    # Проверка на то, что метод convert() приводит datetime к указанному
    # формату
    def test_datetimeconverter_convert_convert_two_datetimes_valid_results(self):
        # Подготовка
        dt1 = datetime.datetime(2025, 6, 1, 12, 30)
        dt2 = datetime.datetime(2000, 10, 10, 0, 5, 30)
        # Действие
        result1 = self.__converter.convert(dt1)
        result2 = self.__converter.convert(dt2)
        # Проверка
        assert result1 == dt1.strftime(DatetimeConverter.format)
        assert result2 == dt2.strftime(DatetimeConverter.format)
    
    # Метод convert() выкинет исключение при передачи неверного типа данных
    def test_datetimeconverter_convert_convert_not_datetime_raise_wrongtype(self):
        # Проверка
        with self.assertRaises(WrongTypeException):
            self.__converter.convert("10.10.2020")


if __name__ == "__main__":
    unittest.main()
