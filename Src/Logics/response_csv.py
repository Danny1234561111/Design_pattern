from typing import List, Any
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_csv(abstract_response):
    delimitter: str = ";"  # Инициализация разделителя

    def create(self, format: str, data: List[Any]) -> str:
        if not data:
            return ""

        fields = common.get_fields(data[0])  # Получаем поля на основе первого элемента
        text = self.delimitter.join(fields) + "\n"  # Формируем заголовок

        for item in data:
            row = [str(item.get(field, '')) for field in fields]  
            text += self.delimitter.join(row) + "\n"  # Добавляем строку с данными

        return text

    def to_dict(self, data: List[Any]) -> list:
        """Преобразовывает данные в список словарей"""
        if not data:
            return []

        fields = common.get_fields(data[0])
        result = []

        for item in data:
            item_dict = {field: item.get(field, '') for field in fields}
            result.append(item_dict)

        return result