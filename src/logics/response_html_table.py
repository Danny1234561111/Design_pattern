# src/core/response_html_table.py (или где находится ResponseHtmlTable)

from typing import List, Any, Dict # Добавил Dict для типа data
from src.core.validator import Validator as vld
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.utils import get_properties, obj_to_str # obj_to_str может понадобиться


"""Класс для формирования ответа в формате HTML Table"""
class ResponseHtmlTable(AbstractResponse):
    
    def __init__(self):
        super().__init__()
    
    # Метод build теперь принимает `headers` и `data`
    def build(self, headers: List[str], data: List[Dict[str, Any]]) -> str:
        # Проверка данных
        if not headers or not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            return "<p>Нет данных для отображения или некорректный формат.</p>"

        html_output = []

        # Заголовок таблицы (может быть общим или динамическим)
        html_output.append("<h1>Отчет оборотно-сальдовой ведомости</h1>") # Общий заголовок

        html_output.append("<table border='1' cellpadding='5' cellspacing='0' style='width:100%; border-collapse: collapse;'>")
        
        # Заголовочная строка таблицы (<th>)
        html_output.append("<thead><tr>")
        html_output.append("<th>#</th>") # Номер строки
        for header_text in headers: # Используем переданные заголовки
            html_output.append(f"<th style='background-color:#f2f2f2; text-align:left; padding:8px;'>{header_text}</th>")
        html_output.append("</tr></thead>")

        # Строки с данными (<td>)
        html_output.append("<tbody>")
        for i, row_data_dict in enumerate(data):
            html_output.append("<tr>")
            html_output.append(f"<td style='padding:8px; border-bottom:1px solid #ddd;'>{i+1}</td>") # Номер строки
            for header_text in headers:
                # Получаем значение по ключу (заголовку) из словаря данных
                value = row_data_dict.get(header_text, '') 
                # obj_to_str может быть полезен, если значения могут быть сложными объектами,
                # но для round(float) он может быть не нужен, если float уже строкоподобен.
                str_value = obj_to_str(value) 
                html_output.append(f"<td style='padding:8px; border-bottom:1px solid #ddd;'>{str_value}</td>")
            html_output.append("</tr>")
        html_output.append("</tbody>")
        
        html_output.append("</table>")
        
        return "".join(html_output) # Используйте .join для эффективности, без \n если не требуется