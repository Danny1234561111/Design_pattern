from typing import Any, Union, Dict, List
from datetime import datetime
from src.core.exceptions import ParamException
from src.core.abstract_model import AbstractModel
from src.core.abstract_converter import AbstractConverter
from src.logics.basic_converter import BasicConverter
from src.logics.datetime_converter import DatetimeConverter
from src.logics.reference_converter import ReferenceConverter
from src.logics.structure_converter import StructureConverter


"""Класс-фабрика для конвертации любых объектов и списков в JSON-формат"""
class FactoryConverters:

    """
    Метод для получения необходимого конвертера по типу переданного объекта
    
    Args:
        object_ (Any): объект, в зависимости от типа которого формируется
            конвертер
    
    Returns:
        AbstractConverter: экземпляр класса-наследника от AbstractConverter
    
    Raises:
        ParamException: для типа переданного объекта фабрика не может
            сформировать конвертер
    """ 
    def create(self, object_: Any) -> AbstractConverter:
        type_ = type(object_)
        if type_ in [bool, int, float, str] or object_ is None:
            return BasicConverter()
        elif type_ is datetime:
            return DatetimeConverter()
        elif isinstance(object_, AbstractModel):
            return ReferenceConverter()
        elif type_ in [list, dict, tuple]:
            return StructureConverter()
        else:
            raise ParamException(
                f"Impossible to create converter from object "
                f"with type '{type_.__name__}'"
            )
    
    """
    Метод-обёртка для получения конвертера из метода create() и вызова
    у него метода convert()
    """
    def convert(self, object_: Any) -> Union[Dict, List]:
        return self.create(object_).convert(object_)
