from typing import Dict, Any
from datetime import datetime
from Src.Core.abstract_convertor import abstract_convertor

class datetime_convertor(abstract_convertor):
    def convert(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, datetime):
            return {"date": obj.strftime("%Y-%m-%d %H:%M:%S")}  # Форматированный дата
        raise ValueError("Unsupported type for datetime convertor")