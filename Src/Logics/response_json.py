import json
from typing import List, Any
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.logics.factory_converters import FactoryConverters
from src.utils import obj_to_dict


"""Класс для формирования ответа в формате Json"""
class ResponseJson(AbstractResponse):
    
    def __init__(self):
        super().__init__()
    
    def build(self, data: List[Any]) -> str:
        super().build(data, ResponseFormat.JSON)

        dict_ = FactoryConverters().convert(data)
        return json.dumps(dict_, ensure_ascii=False)
