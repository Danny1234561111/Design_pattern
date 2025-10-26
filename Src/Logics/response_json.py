import json
from typing import List, Any
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_json(abstract_response):
    """Класс для формирования ответа в формате JSON"""

    def create(self, format: str, data: List[Any]) -> str:
        if not data:
            raise operation_exception("Нет данных для формирования JSON.")

        formatted_data = []
        for item in data:
            fields = common.get_fields(item)  # Получаем поля

            item_dict = {}
            for field in fields:
                value = item.get(field)  # Для словаря используем get
                item_dict[field] = None if value is None else str(value)

            formatted_data.append(item_dict)

        return json.dumps(formatted_data)  # Возвращаем данные в формате JSON

    def to_dict(self, data: List[Any]) -> list:
        """Преобразовывает данные в список словарей"""
        if not data:
            return []

        fields = common.get_fields(data[0])
        result = []

        for item in data:
            item_dict = {}
            for field in fields:
                value = item.get(field)  # Используем get для словаря
                item_dict[field] = value if value is not None else None  # Кладём None, если значение отсутствует
            result.append(item_dict)

        return result