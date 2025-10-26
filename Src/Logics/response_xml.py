from typing import List, Any
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_xml(abstract_response):
    def create(self, format: str, data: List[Any]) -> str:
        xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n'
        
        for item in data:
            xml_string += "  <item>\n"
            fields = common.get_fields(item)  # Получаем поля из текущего элемента
            for field in fields:
                # Используем метод get для словарей, проверяем тип данных
                value = item.get(field, '') if isinstance(item, dict) else getattr(item, field, '')
                xml_string += f"    <{field}>{str(value)}</{field}>\n"
            xml_string += "  </item>\n"

        xml_string += "</root>\n"
        return xml_string  # Возвращаем сформированный XML
    def to_dict(self, data: List[Any]) -> List[dict]:
        if not data:
            return []

        result = []
        # Получаем поля из первого элемента для создания словарей
        fields = common.get_fields(data[0])
        
        for item in data:
            item_dict = {}
            for field in fields:
                # Заполняем словарь значениями
                item_dict[field] = str(item.get(field, '') if isinstance(item, dict) else getattr(item, field, ''))
            result.append(item_dict)
        
        return result