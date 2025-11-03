from typing import Union, List, Tuple, Dict
from src.core.validator import Validator as vld
from src.core.abstract_converter import AbstractConverter


"""Конвертер структур

Обрабатывает объекты, являющиеся списками, кортежами и словарями"""
class StructureConverter(AbstractConverter):
    
    def __init__(self):
        super().__init__()
    
    """Переопределённый метод convert
    
    Получает на вход структуру и конвертирует её значения
    """
    
    
   
    def convert(self, object_: Union[List, Tuple, Dict]) -> Union[List, Dict]:
        from src.logics.factory_converters import FactoryConverters
        
        vld.is_structure(object_, "object")

        factory = FactoryConverters()
        if type(object_) is dict:
            result = dict()
            for key, value in object_.items():
                result[key] = factory.create(value).convert(value)
        else:
            result = list()
            vld.is_list_of_same(object_, "objects", True)
            if len(object_):
                converter = factory.create(object_[0])
                for item in object_:
                    result += [converter.convert(item)]

        return result
