from typing import List, Any
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_md(abstract_response):
    def create(self, format: str, data: List[Any]) -> str:
        if not data:
            return ""

        fields = common.get_fields(data[0])  # Получаем поля на основе первого элемента
        text = "# Данные\n\n"
        text += "| " + " | ".join(fields) + " |\n"  # Заголовок
        text += "| " + " | ".join(["---"] * len(fields)) + " |\n"  # Разделитель для таблицы

        for item in data:
            row = "| " + " | ".join(str(item.get(field, '')) for field in fields) + " |\n"
            text += row

        return text

    def to_dict(self, data: List[Any]) -> list:
        if not data:
            return []

        fields = common.get_fields(data[0])  # Получаем поля
        return [{field: str(item.get(field, '')) for field in fields} for item in data]