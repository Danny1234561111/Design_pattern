from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.response_format import ResponseFormat
from src.models.company_model import CompanyModel
from datetime import date
from typing import Optional, Dict, Any


"""Модель настроек

Инкапсулирует модель компании и настройки приложения.
"""
class SettingsModel(AbstractModel):
    def __init__(self):
        super().__init__()
        # Инициализация всех полей
        self.__company = CompanyModel()
        self.__response_format = ResponseFormat.JSON
        self.__block_date: Optional[date] = None
        self.__first_start: bool = True
        self.__datetime_format: str = "%Y-%m-%d"
        
        # Поля для логирования
        self.__log_level: str = "INFO"
        self.__log_mode: str = "both"
        self.__log_directory: str = "logs"
        self.__log_date_format: str = "%Y-%m-%d %H:%M:%S"
        self.__log_file_prefix: str = "app"
        self.__log_max_size_mb: int = 10
        self.__log_retention_days: int = 30

    """Поле компании"""
    @property
    def company(self) -> CompanyModel:
        return self.__company
    
    @company.setter
    def company(self, value: CompanyModel):
        vld.validate(value, CompanyModel, "company")
        self.__company = value

    """Поле формата ответов"""
    @property
    def response_format(self) -> ResponseFormat:
        return self.__response_format
    
    @response_format.setter
    def response_format(self, value: ResponseFormat):
        vld.validate(value, ResponseFormat, "response_format")
        self.__response_format = value

    """Дата блокировки"""
    @property
    def block_date(self) -> Optional[date]:
        return self.__block_date
    
    @block_date.setter
    def block_date(self, value: date):
        vld.validate(value, date, "block_date")
        self.__block_date = value

    """Первый запуск"""
    @property
    def first_start(self) -> bool:
        return self.__first_start
    
    @first_start.setter
    def first_start(self, value: bool):
        vld.validate(value, bool, "first_start")
        self.__first_start = value

    """Формат даты и времени"""
    @property
    def datetime_format(self) -> str:
        return self.__datetime_format
    
    @datetime_format.setter
    def datetime_format(self, value: str):
        vld.is_str(value, "datetime_format")
        self.__datetime_format = value

    """Уровень логирования (DEBUG, INFO, ERROR)"""
    @property
    def log_level(self) -> str:
        return self.__log_level
    
    @log_level.setter
    def log_level(self, value: str):
        vld.is_str(value, "log_level")
        value = value.upper()
        if value not in ["DEBUG", "INFO", "ERROR"]:
            raise ValueError(f"Недопустимый уровень логирования: {value}")
        self.__log_level = value

    """Режим логирования (console, file, both)"""
    @property
    def log_mode(self) -> str:
        return self.__log_mode
    
    @log_mode.setter
    def log_mode(self, value: str):
        vld.is_str(value, "log_mode")
        value = value.lower()
        if value not in ["console", "file", "both"]:
            raise ValueError(f"Недопустимый режим логирования: {value}")
        self.__log_mode = value

    """Директория для логов"""
    @property
    def log_directory(self) -> str:
        return self.__log_directory
    
    @log_directory.setter
    def log_directory(self, value: str):
        vld.is_str(value, "log_directory")
        self.__log_directory = value

    """Формат даты в логах"""
    @property
    def log_date_format(self) -> str:
        return self.__log_date_format
    
    @log_date_format.setter
    def log_date_format(self, value: str):
        vld.is_str(value, "log_date_format")
        self.__log_date_format = value

    """Префикс файла логов"""
    @property
    def log_file_prefix(self) -> str:
        return self.__log_file_prefix
    
    @log_file_prefix.setter
    def log_file_prefix(self, value: str):
        vld.is_str(value, "log_file_prefix")
        self.__log_file_prefix = value

    """Максимальный размер файла лога в МБ"""
    @property
    def log_max_size_mb(self) -> int:
        return self.__log_max_size_mb
    
    @log_max_size_mb.setter
    def log_max_size_mb(self, value: int):
        vld.validate(value, int, "log_max_size_mb")
        if value <= 0:
            raise ValueError("Максимальный размер файла лога должен быть больше 0")
        self.__log_max_size_mb = value

    """Дни хранения логов"""
    @property
    def log_retention_days(self) -> int:
        return self.__log_retention_days
    
    @log_retention_days.setter
    def log_retention_days(self, value: int):
        vld.validate(value, int, "log_retention_days")
        if value <= 0:
            raise ValueError("Дни хранения логов должны быть больше 0")
        self.__log_retention_days = value

    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует модель в словарь"""
        return {
            "company": self.company.to_dict(),
            "block_date": self.block_date.strftime("%Y-%m-%d") if self.block_date else None,
            "first_start": self.first_start,
            "datetime_format": self.datetime_format,
            "response_format": self.response_format.value,
            "log_level": self.log_level,
            "log_mode": self.log_mode,
            "log_directory": self.log_directory,
            "log_date_format": self.log_date_format,
            "log_file_prefix": self.log_file_prefix,
            "log_max_size_mb": self.log_max_size_mb,
            "log_retention_days": self.log_retention_days
        }

    def from_dict(self, data: Dict[str, Any]) -> 'SettingsModel':
        """Загружает модель из словаря"""
        vld.is_dict(data, "data")
        
        # Загрузка данных компании
        if "company" in data:
            self.company.from_dict(data["company"])
        
        # Загрузка блока даты
        if "block_date" in data and data["block_date"]:
            try:
                from datetime import datetime
                self.block_date = datetime.strptime(data["block_date"], "%Y-%m-%d").date()
            except ValueError:
                try:
                    self.block_date = datetime.strptime(data["block_date"], "%d.%m.%Y").date()
                except ValueError as e:
                    raise ValueError(f"Неподдерживаемый формат даты: {data['block_date']}")
        
        # Загрузка остальных полей
        if "first_start" in data:
            self.first_start = bool(data["first_start"])
        
        if "datetime_format" in data:
            self.datetime_format = data["datetime_format"]
        
        if "response_format" in data:
            from src.logics.factory_entities import FactoryEntities
            format_str = data["response_format"]
            if format_str in FactoryEntities.match_formats:
                self.response_format = FactoryEntities.match_formats[format_str]
        
        # Загрузка настроек логирования
        if "log_level" in data:
            self.log_level = data["log_level"]
        
        if "log_mode" in data:
            self.log_mode = data["log_mode"]
        
        if "log_directory" in data:
            self.log_directory = data["log_directory"]
        
        if "log_date_format" in data:
            self.log_date_format = data["log_date_format"]
        
        if "log_file_prefix" in data:
            self.log_file_prefix = data["log_file_prefix"]
        
        if "log_max_size_mb" in data:
            self.log_max_size_mb = int(data["log_max_size_mb"])
        
        if "log_retention_days" in data:
            self.log_retention_days = int(data["log_retention_days"])
        
        return self