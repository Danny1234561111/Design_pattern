# datetime_convertor.py

from typing import Dict, Any
from datetime import datetime
from Src.Core.abstract_convertor import abstract_convertor

class datetime_convertor(abstract_convertor):
    def Convert(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, datetime):
            return {"date": obj.strftime("%Y-%m-%d %H:%M:%S")}
        raise ValueError("Unsupported type for datetime convertor")