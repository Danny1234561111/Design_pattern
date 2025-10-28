from typing import Any, Union, Dict, List, Type, Tuple
from datetime import datetime
from Src.Core.exceptions import ParamException
from Src.Core.abstract_model import abstact_model
from Src.Core.abstract_convertor import abstract_convertor
from Src.Convert.basic_convertor import basic_convertor
from Src.Convert.datetime_convertor import datetime_convertor
from Src.Convert.reference_convertor import reference_convertor
from Src.Core import validator as vld


"""Конвертер структур

Обрабатывает объекты, являющиеся списками, кортежами и словарями"""
class StructureConvertor(abstract_convertor):
    """Переопределённый метод convert

    Получает на вход структуру и конвертирует её значения
    """
    def convert(self, object_: Union[List, Tuple, Dict]) -> Union[List, Dict]:
        # Импорт FactoryConverters здесь для избежания циклического импорта
        from Src.Convert.convert_factory import FactoryConvertors
        vld.validator

        vld.is_structure(object_, "object")

        factory = FactoryConvertors()  # Создаем экземпляр FactoryConverters здесь

        if isinstance(object_, dict):
            result = {}
            for key, value in object_.items():
                result[key] = factory.convert(value)  # Используем convert для рекурсивного вызова
            return result
        elif isinstance(object_, (list, tuple)):
            result = []
            for item in object_:
                result.append(factory.convert(item))  # Используем convert для рекурсивного вызова
            return result
        else:
            raise ParamException(f"Unsupported structure type: {type(object_)}")