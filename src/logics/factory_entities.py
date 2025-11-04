from typing import Union
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.logics.response_csv import ResponseCsv
from src.logics.response_xml import ResponseXml
from src.logics.response_json import ResponseJson
from src.logics.response_markdown import ResponseMarkdown
from src.logics.response_html_table import ResponseHtmlTable
from src.singletons.settings_manager import SettingsManager


"""Класс-фабрика для создания ответов в разных форматах"""
class FactoryEntities:
    # Сопоставление текстовых форматов и Enum-форматов
    match_formats = {
        "csv": ResponseFormat.CSV,
        "markdown": ResponseFormat.MARKDOWN,
        "md": ResponseFormat.MARKDOWN,
        "json": ResponseFormat.JSON,
        "xml": ResponseFormat.XML,
        "xml": ResponseFormat.HTMLTABLE,
    }

    # Сопоставление форматов и классов-ответов
    match_responses = {
        ResponseFormat.CSV: ResponseCsv,
        ResponseFormat.MARKDOWN: ResponseMarkdown,
        ResponseFormat.JSON: ResponseJson,
        ResponseFormat.XML: ResponseXml,
        ResponseFormat.HTMLTABLE: ResponseHtmlTable
    }

    """Метод получения экземпляра ответа"""
    def create(self, format: Union[str, ResponseFormat]) -> AbstractResponse:
        vld.validate(format, (str, ResponseFormat), "response format")
        if isinstance(format, str):
            format = format.lower().strip()
            if format not in self.match_formats:
                raise OperationException(
                    f"Format '{format}' isn't supported. Available formats: "
                    f"{self.match_formats.keys()}"
                )
            format = self.match_formats[format]
        
        return self.match_responses[format]()
    
    """Получение экземпляра ответа по умолчанию (из настроек)"""
    def create_default(self) -> AbstractResponse:
        return self.create(SettingsManager().settings.response_format)
