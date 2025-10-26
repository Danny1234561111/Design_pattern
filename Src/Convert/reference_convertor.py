# reference_convertor.py

from typing import Dict, Any
from Src.Core.abstract_convertor import abstract_convertor

class reference_convertor(abstract_convertor):
    def Convert(self, obj: Any) -> Dict[str, Any]:
        if hasattr(obj, 'id') and hasattr(obj, 'name'):
            return {"id": obj.id, "name": obj.name}
        raise ValueError("Unsupported type for reference convertor")