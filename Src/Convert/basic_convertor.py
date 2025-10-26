# basic_convertor.py

from typing import Dict, Any
from Src.Core.abstract_convertor import abstract_convertor

class basic_convertor(abstract_convertor):
    def Convert(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, (str, int, float)):
            return {"value": obj}
        raise ValueError("Unsupported type for basic convertor")