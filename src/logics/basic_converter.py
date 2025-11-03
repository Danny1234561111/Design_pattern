from typing import Union
from src.core.validator import Validator as vld
from src.core.abstract_converter import AbstractConverter


"""Конвертер, обрабатывающий примитивные типы данных"""
class BasicConverter(AbstractConverter):
    
    def __init__(self):
        super().__init__()
    
    """Переопределённый метод convert
    
    Для примитивных типов не делает никакого преобразования
    """
    def convert(self, object_: Union[str, int, float, bool, None]):
        vld.validate(object_, (str, int, float, bool), "object", True)

        return object_
