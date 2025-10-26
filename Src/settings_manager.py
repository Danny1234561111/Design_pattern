import json
import os
from Src.Core.validator import validator
from Src.Core.response_format import ResponseFormat
from Src.Models.settings_model import settings_model
from Src.Models.company_model import company_model

"""Менеджер настроек

Предназначен для управления настройками и хранения параметров приложения.
"""
class settings_manager:
    # Ссылка на экземпляр SettingsManager
    __instance = None

    # Абсолютный путь до файла с загруженными настройками
    __file_name: str = ""

    # Инкапсулируемый объект настроек
    __settings: settings_model = None  # Initialize to None

    def __init__(self):
        self.default()

    @classmethod
    def new(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    """Абсолютный путь к файлу с настройками"""
    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if not os.path.isfile(value):
            raise FileNotFoundError(f"Файл '{value}' не существует.")
        self.__file_name = value

    """Настройки с хранящейся моделью компании"""
    @property
    def settings(self) -> settings_model:
        return self.__settings

    @settings.setter
    def settings(self, value: settings_model):
        validator.validate(value, settings_model, "settings")
        self.__settings = value

    """Метод загрузки файла настроек"""
    def load(self, file_name: str) -> bool:
        try:
            self.file_name = file_name  # Сначала устанавливаем file_name
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                settings = json.load(file)
                print("Настройки загружены:", settings)  # Отладка: посмотреть загруженные настройки
                if "company" in settings:
                    return self.convert(settings["company"])  # Теперь convert доступен
                else:
                    return False  # Если нет ключа "company", то возвращаем False
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке настроек: {e}")
            return False

    """Метод извлечения данных компании из загруженного файла настроек"""
    def convert(self, data: dict) -> bool:
        validator.is_dict(data, "data")

        # Поля модели компании, которые могут быть заполнены
        company_model_fields = [
            field for field in dir(self.settings.company)
            if not field.startswith("_") and not field.startswith("__")
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
        except Exception as e:
            print(f"Ошибка при конвертации данных компании: {e}")
            return False

    """Метод инициализации стандартных значений полей"""
    def default(self):
        self.__settings = settings_model()
        if self.__settings.company is None:
            self.__settings.company = company_model()