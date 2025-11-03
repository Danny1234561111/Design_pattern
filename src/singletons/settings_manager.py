import json
from src.core.validator import Validator as vld
from src.models.settings_model import SettingsModel


"""Менеджер настроек

Предназначен для управления настройками и хранения параметров приложения.
"""
class SettingsManager:
    # Ссылка на экземпляр SettingsManager
    __instance = None

    # Абсолютный путь до файла с загруженными настройками
    __file_name: str = ""

    # Инкупсулирумый объект настроек
    __settings: SettingsModel

    def __init__(self):
        self.default()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Абсолютный путь к файлу с настройками"""
    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = vld.is_file_exists(value)
    
    """Настройки с хранящейся моделью компании"""
    @property
    def settings(self) -> SettingsModel:
        return self.__settings

    @settings.setter
    def settings(self, value: SettingsModel):
        vld.validate(value, SettingsModel, "settings")
        self.__settings = value
    
    """Метод загрузки файла настроек"""
    def load(self, file_name: str) -> bool:
        self.file_name = file_name
        try:
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                settings = json.load(file)
                self.convert_company_data(settings["company"])
                self.convert_response_format(settings["default_response_format"])

                # Проверяем, нужно ли загружать данные при первом старте
                if settings.get("first_start", False):
                    pass

                return True
        except Exception as e:
            return False
    
    """Метод извлечения данных компании из загуженного файла настроек"""
    def convert_company_data(self, data: dict) -> bool:
        vld.is_dict(data, "data")

        # Поля модели компании, которые могут быть заполнены
        company_model_fields = [
            field for field in dir(self.settings.company)
            if not field.startswith("_")
        ]
        # Ключи загруженного объекта настроек
        matching_keys = [
            key for key in data.keys()
            if key in company_model_fields
        ]

        try:
            for key in matching_keys:
                setattr(self.settings.company, key, data[key])
            return True
        except:
            return False
    
    """Метод загрузки формата ответов по умолчанию из файла настроек"""
    def convert_response_format(self, data: str) -> bool:
        from src.logics.factory_entities import FactoryEntities
        try:
            format = FactoryEntities.match_formats[data]
            self.settings.response_format = format
            return True
        except KeyError:
            return False
    
    """Метод инициализации стандартных значений полей"""
    def default(self):
        self.settings = SettingsModel()
        self.settings.company.name = "Default Name"
        self.settings.company.ownership = "owner"
