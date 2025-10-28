# abstract_covertor.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class abstract_convertor(ABC):
    @abstractmethod
    def convert(self, obj: Any) -> Dict[str, Any]:
        pass