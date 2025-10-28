from typing import Any, Dict, List, Tuple, Union
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import validator as vld

from Src.Core.exceptions import ParamException

class StructureConvertor(abstract_convertor):
    """Переопределённый метод convert

    Получает на вход структуру и конвертирует её значения
    """
    def convert(self, object_: Union[List, Tuple, Dict]) -> Union[List, Dict]:
        from Src.Convert.convert_factory import FactoryConvertors
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