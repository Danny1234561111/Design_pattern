# Src/Models/settings_model.py
from Src.Models.company_model import company_model
from Src.Core.validator import validator
from Src.Core.response_format import ResponseFormat

####################################### Модель настроек приложения
class settings_model:
    def __init__(self, company: company_model = None, response_format: ResponseFormat = ResponseFormat.JSON):
        self.__company = None  # Инициализируем перед использованием сеттера
        self.__response_format = None  # Инициализируем перед использованием сеттера
        self.company = company
        self.response_format = response_format

    __company: company_model = None
    __response_format: ResponseFormat

    # Текущая организация
    @property
    def company(self) -> company_model:
        return self.__company

    @company.setter
    def company(self, value: company_model):
        if value is not None:  # Проверяем, что value не None
            validator.validate(value, company_model)
            self.__company = value
        else:
            self.__company = None

    """Поле формата ответов"""
    @property
    def response_format(self) -> ResponseFormat:
        return self.__response_format

    @response_format.setter
    def response_format(self, value: ResponseFormat):
        if value is not None: # Проверяем что value не None
            validator.validate(value, ResponseFormat, "response format")
            self.__response_format = value
        else:
            self.__response_format = ResponseFormat.JSON # Или какое-то значение по умолчанию
