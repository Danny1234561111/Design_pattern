from datetime import datetime 
from src.core.validator import Validator as vld
from src.core.abstract_converter import AbstractConverter


"""Конвертер класса datetime.datetime

Приводит объекты datetime к строковому представлению"""
class DatetimeConverter(AbstractConverter):

    # Строковый формат datetime
    format: str = "%Y-%m-%d %H:%M:%S"
    
    def __init__(self):
        super().__init__()
    
    """Переопределённый метод convert
    
    Приводит datetime к строковому представлению в заданном формате"""
    def convert(self, object_: datetime) -> str:
        vld.validate(object_, datetime, "object")

        return object_.strftime(DatetimeConverter.format)
