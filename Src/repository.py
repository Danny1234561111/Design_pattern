"""Репозиторий данных"""
class Repository:
    # Словарь наименований моделей
    __data = dict()

    @property
    def data(self) -> dict:
        return self.__data

    """Ключ для единиц измерения"""
    @staticmethod
    def measure_unit_key():
        return "range_model"