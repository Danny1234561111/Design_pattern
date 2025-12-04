import json
from src.core.validator import Validator as vld
from src.models.settings_model import SettingsModel
from datetime import date, datetime
from src.core.abstract_subscriber import AbstractSubscriber
from src.core.observe_service import observe_service
from src.core.event_type import event_type

"""Менеджер настроек

Предназначен для управления настройками и хранения параметров приложения.
"""
class SettingsManager(AbstractSubscriber):
    # Ссылка на экземпляр SettingsManager
    __instance = None

    # Абсолютный путь до файла с загруженными настройками
    __file_name: str = ""

    # Инкапсулируемый объект настроек
    __settings: SettingsModel

    def __init__(self):
        self.default()
        observe_service.add(self)

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
                
                # Загружаем блоки настроек
                self.__load_company_data(settings.get("company", {}))
                self.__load_response_format(settings.get("default_response_format", "json"))
                self.__load_app_settings(settings)
                self.__load_logging_settings(settings.get("logging", {}))
                
                # Проверяем, нужно ли загружать данные при первом старте
                if settings.get("first_start", False):
                    # Можно выполнить дополнительные действия при первом старте
                    pass

                # Логируем успешную загрузку настроек
                observe_service.create_event(event_type.settings_updated(), {
                    "operation": "load_settings",
                    "file": file_name,
                    "status": "success"
                })
                
                return True
        except Exception as e:
            # Логируем ошибку загрузки
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "load_settings",
                "file": file_name,
                "status": "error",
                "error": str(e)
            })
            raise
    
    """Метод сохранения настроек в файл"""
    def save(self, file_name: str = None) -> bool:
        try:
            save_file = file_name if file_name else self.file_name
            if not save_file:
                raise ValueError("Не указан файл для сохранения настроек")
            
            # Подготавливаем данные для сохранения
            data = self.__prepare_save_data()
            
            with open(save_file, mode='w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            # Логируем успешное сохранение
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "save_settings",
                "file": save_file,
                "status": "success"
            })
            
            return True
        except Exception as e:
            # Логируем ошибку сохранения
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "save_settings",
                "status": "error",
                "error": str(e)
            })
            raise
    
    def __load_company_data(self, data: dict) -> bool:
        """Метод загрузки данных компании из файла настроек"""
        vld.is_dict(data, "data")

        # Поля модели компании, которые могут быть заполнены
        company_model_fields = [
            field for field in dir(self.settings.company)
            if not field.startswith("_") and not callable(getattr(self.settings.company, field))
        ]
        
        try:
            for key in data.keys():
                if key in company_model_fields:
                    setattr(self.settings.company, key, data[key])
            return True
        except Exception as e:
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "load_company_data",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def __load_response_format(self, format_str: str) -> bool:
        """Метод загрузки формата ответов по умолчанию из файла настроек"""
        from src.logics.factory_entities import FactoryEntities
        try:
            format = FactoryEntities.match_formats[format_str]
            self.settings.response_format = format
            return True
        except KeyError as e:
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "load_response_format",
                "status": "error",
                "error": f"Неподдерживаемый формат: {format_str}"
            })
            return False
    
    def __load_app_settings(self, data: dict) -> bool:
        """Загрузка общих настроек приложения"""
        try:
            # Загружаем block_date
            if "block_date" in data:
                # Пробуем разные форматы даты
                block_date_str = data["block_date"]
                try:
                    self.settings.block_date = datetime.strptime(block_date_str, "%Y-%m-%d").date()
                except ValueError:
                    try:
                        self.settings.block_date = datetime.strptime(block_date_str, "%d.%m.%Y").date()
                    except ValueError:
                        raise ValueError(f"Неподдерживаемый формат даты: {block_date_str}")
            
            # Загружаем first_start
            if "first_start" in data:
                self.settings.first_start = bool(data["first_start"])
            
            # Загружаем datetime_format
            if "datetime_format" in data:
                self.settings.datetime_format = data["datetime_format"]
            
            return True
        except Exception as e:
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "load_app_settings",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def __load_logging_settings(self, data: dict) -> bool:
        """Загрузка настроек логирования"""
        try:
            # Уровень логирования
            if "log_level" in data:
                level = data["log_level"].upper()
                if level in ["DEBUG", "INFO", "ERROR"]:
                    self.settings.log_level = level
                else:
                    self.settings.log_level = "INFO"
            
            # Режим логирования
            if "log_mode" in data:
                mode = data["log_mode"].lower()
                if mode in ["console", "file", "both"]:
                    self.settings.log_mode = mode
                else:
                    self.settings.log_mode = "both"
            
            # Директория логов
            if "log_directory" in data:
                self.settings.log_directory = data["log_directory"]
            
            # Формат даты в логах
            if "log_date_format" in data:
                self.settings.log_date_format = data["log_date_format"]
            
            # Префикс файла логов
            if "log_file_prefix" in data:
                self.settings.log_file_prefix = data["log_file_prefix"]
            
            # Максимальный размер файла (в МБ)
            if "log_max_size_mb" in data:
                self.settings.log_max_size_mb = int(data["log_max_size_mb"])
            
            # Хранение логов (в днях)
            if "log_retention_days" in data:
                self.settings.log_retention_days = int(data["log_retention_days"])
            
            return True
        except Exception as e:
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "load_logging_settings",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def __prepare_save_data(self) -> dict:
        """Подготовка данных для сохранения в файл"""
        # Базовые настройки
        data = {
            "company": {
                "name": self.settings.company.name,
                "inn": self.settings.company.inn,
                "account": self.settings.company.account,
                "corr_account": self.settings.company.corr_account,
                "bic": self.settings.company.bic,
                "ownership": self.settings.company.ownership
            },
            "block_date": self.settings.block_date.strftime("%Y-%m-%d"),
            "first_start": self.settings.first_start,
            "datetime_format": self.settings.datetime_format,
            "default_response_format": "json",
        }
        
        # Добавляем настройки логирования, если они есть
        if hasattr(self.settings, 'log_level'):
            data["logging"] = {
                "log_level": self.settings.log_level,
                "log_mode": self.settings.log_mode,
                "log_directory": self.settings.log_directory,
                "log_date_format": self.settings.log_date_format,
                "log_file_prefix": self.settings.log_file_prefix
            }
            
            # Опциональные параметры
            if hasattr(self.settings, 'log_max_size_mb'):
                data["logging"]["log_max_size_mb"] = self.settings.log_max_size_mb
            
            if hasattr(self.settings, 'log_retention_days'):
                data["logging"]["log_retention_days"] = self.settings.log_retention_days
        
        return data
    
    """Метод инициализации стандартных значений полей"""
    def default(self):
        self.settings = SettingsModel()
        self.settings.company.name = "Default Name"
        self.settings.company.ownership = "owner"
        self.settings.block_date = date.today()
        self.settings.first_start = True
        self.settings.datetime_format = "%Y-%m-%d"
        
        # Настройки логирования по умолчанию
        self.settings.log_level = "INFO"
        self.settings.log_mode = "both"
        self.settings.log_directory = "logs"
        self.settings.log_date_format = "%Y-%m-%d %H:%M:%S"
        self.settings.log_file_prefix = "app"
        self.settings.log_max_size_mb = 10
        self.settings.log_retention_days = 30
    
    """Обновление настроек логирования"""
    def update_logging_settings(self, settings: dict) -> bool:
        try:
            # Валидация входных данных
            vld.is_dict(settings, "settings")
            
            # Обновляем настройки
            updated = False
            for key, value in settings.items():
                if hasattr(self.settings, key):
                    setattr(self.settings, key, value)
                    updated = True
            
            # Сохраняем изменения
            if updated:
                self.save()
                
                # Логируем обновление
                observe_service.create_event(event_type.settings_updated(), {
                    "operation": "update_logging_settings",
                    "settings": settings,
                    "status": "success"
                })
            
            return updated
        except Exception as e:
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "update_logging_settings",
                "status": "error",
                "error": str(e)
            })
            raise
    
    """
    Обработка событий
    """
    def handle(self, event: str, params: dict):
        vld.validate(params, dict, "params")
        super().handle(event, params)

        if event == event_type.change_block_period():
            new_block_date = params["new_block_date"]
            vld.validate(new_block_date, (date, datetime), "new_block_date")
            
            # Если пришел datetime, преобразуем в date
            if isinstance(new_block_date, datetime):
                new_block_date = new_block_date.date()
            
            # Обновляем block_date
            self.settings.block_date = new_block_date
            
            # Сохраняем настройки
            self.save()
            
            # Логируем изменение
            observe_service.create_event(event_type.settings_updated(), {
                "operation": "change_block_period",
                "new_block_date": new_block_date.strftime("%Y-%m-%d"),
                "status": "success"
            })
        
        elif event == event_type.settings_updated():
            # Реагируем на обновление настроек
            operation = params.get("operation", "unknown")
            status = params.get("status", "unknown")
            
            if status == "error":
                error = params.get("error", "unknown")
                # Можно добавить дополнительную обработку ошибок
                pass