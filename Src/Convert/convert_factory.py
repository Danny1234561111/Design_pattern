# convert_factory.py

from typing import Any, List
from Src.Convert.basic_convertor import basic_convertor
from Src.Convert.datetime_convertor import datetime_convertor
from Src.Convert.reference_convertor import reference_convertor
from datetime import datetime

class convert_factory:
    def __init__(self):
        self.converters = {
            'basic': basic_convertor(),
            'datetime': datetime_convertor(),
            'reference': reference_convertor()
        }

    def Convert(self, obj: Any) -> List[dict]:
        result = []
        if isinstance(obj, list):
            for item in obj:
                result.append(self._convert_item(item))
        else:
            result.append(self._convert_item(obj))
        return result

    def _convert_item(self, item: Any) -> dict:
        try:
            if isinstance(item, (str, int, float)):
                return self.converters['basic'].Convert(item)
            elif isinstance(item, datetime):
                return self.converters['datetime'].Convert(item)
            else:
                return self.converters['reference'].Convert(item)
        except ValueError:
            return {}