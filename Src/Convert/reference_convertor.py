from typing import Any, Dict
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.common import common

class reference_convertor(abstract_convertor):
    def convert(self, obj: Any) -> Dict[str, Any]:
        from Src.Convert.convert_factory import FactoryConvertors  # Перемещено внутрь метода

        factory = FactoryConvertors()
        result = {}

        fields = common.get_fields(obj)  # Получаем все поля с помощью get_fields
        
        for property in fields:  # Получаем только имена полей
            value = getattr(obj, property, None)  # Получаем само значение поля
            if value is None:
                print(f"Warning: {property} has no value.")
            else:
                print(f"Converting property: {property} with value: {value}")
            result[property] = factory.convert(value)  # Конвертируем значение

        return result