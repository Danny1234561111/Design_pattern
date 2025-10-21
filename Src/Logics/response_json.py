from typing import List, Any
import json
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_json(abstract_response):
    """Класс для формирования ответа в формате JSON"""

    def create(self, format: str, data: List[Any]) -> str:
        # Проверка на наличие данных
        if not data:
            raise operation_exception("Нет данных для формирования JSON.")

        # Шапка (получаем поля из первого элемента)
        item = data[0]
        fields = common.get_fields(item)

        # Форматирование значений
        def format_value(value):
            if hasattr(value, 'unique_code'):
                return str(value.unique_code)
            else:
                return value

        # Данные
        formatted_data = []
        for item in data:
            item_dict = {}
            item_fields = common.get_fields(item)

            if fields != item_fields:
                raise operation_exception("Количество и/или названия полей объектов не совпадают.")

            for field in fields:
                value = getattr(item, field)
                if isinstance(value, list):
                    item_dict[field] = [format_value(v) for v in value]
                else:
                    item_dict[field] = format_value(value)

            formatted_data.append(item_dict)

        return json.dumps(formatted_data, indent=4)
