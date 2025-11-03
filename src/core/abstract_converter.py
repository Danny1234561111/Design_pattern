from abc import ABC, abstractmethod
from typing import Any


"""Абстракный класс конвертера моделей в объекты JSON"""
class AbstractConverter(ABC):

    @abstractmethod
    def __init__(self):
        super().__init__()
    
    """Абстракный метод для конвертации"""
    @abstractmethod
    def convert(self, object_: Any) -> dict:
        pass
