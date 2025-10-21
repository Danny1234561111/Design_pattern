from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import operation_exception

class response_md(abstract_response):
    """Класс для формирования ответов в формате Markdown"""

    # Сформировать Markdown
    def create(self, format: str, data: list):
        text = super().create(format, data)

        if not data:
            return text  # Если нет данных, возвращаем пустой текст

        # Добавляем заголовок первого уровня
        text = "# Данные\n\n"  + text

        # Шапка
        item = data[0]
        fields = common.get_fields(item)
        text += "| " + " | ".join(fields) + " |\n"  # Формируем заголовок
        text += "| " + " | ".join(["---"] * len(fields)) + " |\n"  # Разделитель

        # Форматирование значения
        def format_value(value):
            if hasattr(value, 'unique_code'):
                return str(value.unique_code)
            else:
                return str(value)

        # Данные
        for item in data:
            field_values = {}
            item_fields = common.get_fields(item)
            if fields != item_fields:
                raise operation_exception("Количество и/или названия полей объектов не совпадают.")
            for field in fields:
                value = getattr(item, field)
                field_values[field] = format_value(value)

            # Формируем строку для Markdown
            row = "| " + " | ".join(field_values[field] for field in fields) + " |\n"
            text += row

        return text