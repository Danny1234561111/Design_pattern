from typing import Any, Dict
from datetime import datetime
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.validator import argument_exception

class datetime_convertor(abstract_convertor):
    def convert(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, datetime):
            return {"date": obj.strftime("%Y-%m-%d %H:%M:%S")}  # Форматированный дата
        
        raise argument_exception("Unsupported type for datetime convertor")  # Использование вашего исключения