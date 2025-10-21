from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_csv(abstract_response):
    delimitter:str = ";" # Инициализация разделителя

    # Сформировать CSV
    def create(self, format: str, data: list):
        text = super().create(format, data)

        # Шапка
        item = data[0]
        fields = common.get_fields(item)
        text += self.delimitter.join(fields) + "\n"  # Формируем заголовок и добавляем его

        # Форматирование значения
        def format_value(value):
            if hasattr(value, 'unique_code'):
                return str(value.unique_code)
            else:
                return str(value)

        # Данные
        for item in data:
            field_values = {}
            max_list_length = 1
            item_fields = common.get_fields(item)
            if fields != item_fields:
                raise operation_exception("Количество и/или названия полей объектов не совпадают.")
            for field in fields:
                value = getattr(item, field)
                if isinstance(value, list):
                    field_values[field] = [format_value(v) for v in value]
                    max_list_length = max(max_list_length, len(value))
                else:
                    field_values[field] = [format_value(value)]
            for i in range(max_list_length):
                for field in fields:
                    values = field_values[field]
                    if i < len(values):
                        text += f"{values[i]}{self.delimitter}"  # Используем delimitter
                    else:
                        text += f"{self.delimitter}"  # Используем delimitter
                text += "\n"

        return text
