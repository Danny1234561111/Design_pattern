from Src.Core.common import common

"""
Репозиторий данных
"""
class reposity:
    __data = {}

    @property
    def data(self):
        return self.__data
    
    @staticmethod
    def range_key():
        return "range_model"
    
    @staticmethod
    def group_key():
        return "group_model"
    
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"
    
    @staticmethod
    def receipt_key():
        return "receipt_model"
    
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(reposity) if callable(getattr(reposity, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)
        return result

    def initialize(self):  # Исправлено название
        keys = reposity.keys()
        for key in keys:
            self.__data[key] = []