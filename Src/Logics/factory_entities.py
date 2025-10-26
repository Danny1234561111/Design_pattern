from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
from Src.Core.validator import validator, operation_exception
from Src.Models.settings_model import settings_model
from Src.Core.response_format import ResponseFormat
from Src.settings_manager import settings_manager

class factory_entities:
    __match = {
        ResponseFormat.CSV: response_csv,
        ResponseFormat.MARKDOWN: response_md,
        ResponseFormat.XML: response_xml,
        ResponseFormat.JSON: response_json
    }
    
    @staticmethod
    def create(format: str | ResponseFormat) -> abstract_response:
        if isinstance(format, str):
            try:
                format = ResponseFormat(format.upper())
            except ValueError:
                raise operation_exception("Формат не верный")

        if format not in factory_entities.__match.keys():
            raise operation_exception("Формат не верный")

        return factory_entities.__match[format]()

    @staticmethod
    def create_default() -> abstract_response:
        settings = settings_manager().settings
        return factory_entities.create(settings.response_format)

    @staticmethod
    def create_response(format: str | ResponseFormat, data) -> str:
        response = factory_entities.create(format) 
        return response.create(format, data)  # Используем create для формирования ответа