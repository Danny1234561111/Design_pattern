from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.response_format import ResponseFormat
from src.models.company_model import CompanyModel


"""Модель настроек

Инкапсулирует модель компании.
"""
class SettingsModel(AbstractModel):
    # Ссылка на объект модели компании
    __company: CompanyModel = None

    # Формат ответов (по умолчанию JSON)
    __response_format: ResponseFormat

    def __init__(self):
        super().__init__()
        self.__company = CompanyModel()
        self.__response_format = ResponseFormat.JSON

    """Поле компании"""
    @property
    def company(self) -> CompanyModel:
        return self.__company
    
    """Поле формата ответов"""
    @property
    def response_format(self) -> ResponseFormat:
        return self.__response_format
    
    @response_format.setter
    def response_format(self, value: ResponseFormat):
        vld.validate(value, ResponseFormat, "response format")
        self.__response_format = value
