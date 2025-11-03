from typing import List, Any
from src.core.validator import Validator as vld
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.utils import get_properties, obj_to_str


"""Класс для формирования ответа в формате CSV"""
class ResponseCsv(AbstractResponse):
    # Разделитель CSV
    delimitter: str = ","

    def __init__(self):
        super().__init__()
    
    """Сформировать CSV из списка моделей"""
    def build(self, data: List[Any]) -> str:
        text = super().build(data, ResponseFormat.CSV)

        # Шапка
        item = data[0]
        properties = get_properties(item)
        text += self.delimitter.join(properties) + "\n"
        
        # Данные
        rows = list()
        for item in data:
            values = list()
            for prop in properties:
                value = getattr(item, prop)
                values += [obj_to_str(value)]
            
            rows += [self.delimitter.join(values)]
        
        text += "\n".join(rows)
        return text
