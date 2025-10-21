from typing import List, Any
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_xml(abstract_response):
    """Класс для формирования ответа в формате XML"""
    
    def create(self,format: str, data: List[Any]) -> str:
        xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_string += "<root>\n"  # Добавляем корневой элемент

        if not data:
            xml_string += "</root>\n"
            return xml_string

        # Проверяем, что все элементы в data имеют одинаковый тип
        first_type = type(data[0])
        for item in data:
            if type(item) != first_type:
                raise operation_exception("Все элементы в списке data должны быть одного типа.")
        
        for item in data:
            xml_string += "  <item>\n"
            fields = common.get_fields(item)  # Получаем поля объекта
            for field in fields:
                value = getattr(item, field)
                xml_string += f"    <{field}>{self.format_value(value)}</{field}>\n"
            xml_string += "  </item>\n"
        
        xml_string += "</root>\n"  # Закрываем корневой элемент
        return xml_string
    
    def format_value(self, value: Any) -> str:
        """Форматирует значение для XML"""
        if hasattr(value, 'unique_code'):
            return str(value.unique_code)
        return str(value)

