from src.core.abstract_logic import abstract_logic
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.singletons.settings_manager import SettingsManager
import os
import json
from datetime import datetime, date
from enum import Enum
from typing import Dict, Any, Optional

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"

class LogMode(Enum):
    CONSOLE = "console"
    FILE = "file"
    BOTH = "both"

class print_service(abstract_logic):
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
            self._settings_manager = SettingsManager()
            self._current_log_file = None
            
            # Загружаем настройки
            self._load_settings()
            
            # Подключение к наблюдению
            observe_service.add(self)
    
    def _load_settings(self):
        """Загружает настройки логирования"""
        try:
            # Настройки из SettingsManager
            settings = self._settings_manager.settings
            
            # Уровень логирования
            log_level = settings.log_level.upper()
            if log_level not in [l.value for l in LogLevel]:
                log_level = "INFO"
            self.log_level = LogLevel(log_level)
            
            # Режим логирования
            log_mode = settings.log_mode.lower()
            if log_mode not in [m.value for m in LogMode]:
                log_mode = "both"
            self.log_mode = LogMode(log_mode)
            
            # Директория для логов
            self.log_directory = settings.log_directory
            
            # Формат даты
            self.date_format = settings.log_date_format
            
            # Префикс файла
            self.log_file_prefix = settings.log_file_prefix
            
            # Максимальный размер файла и дни хранения
            self.log_max_size_mb = getattr(settings, 'log_max_size_mb', 10)
            self.log_retention_days = getattr(settings, 'log_retention_days', 30)
            
            # Создаем директорию для логов если не существует
            if self.log_mode in [LogMode.FILE, LogMode.BOTH]:
                os.makedirs(self.log_directory, exist_ok=True)
                self._rotate_log_file()
                
            # Логируем загрузку настроек
            self._write_log(LogLevel.INFO, "Logging settings loaded", {
                "log_level": self.log_level.value,
                "log_mode": self.log_mode.value,
                "log_directory": self.log_directory
            })
                
        except Exception as e:
            # Значения по умолчанию при ошибке
            self.log_level = LogLevel.INFO
            self.log_mode = LogMode.BOTH
            self.log_directory = "logs"
            self.date_format = "%Y-%m-%d %H:%M:%S"
            self.log_file_prefix = "app"
            self.log_max_size_mb = 10
            self.log_retention_days = 30
            
            os.makedirs(self.log_directory, exist_ok=True)
            
            self._write_log(LogLevel.ERROR, "Error loading logging settings", {
                "error": str(e),
                "using_defaults": True
            })
    
    def _rotate_log_file(self):
        """Ротация лог-файла по дням"""
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"{self.log_file_prefix}_{today}.log"
        self._current_log_file = os.path.join(self.log_directory, filename)
        
        # Проверяем размер файла и ротируем при необходимости
        if os.path.exists(self._current_log_file):
            file_size_mb = os.path.getsize(self._current_log_file) / (1024 * 1024)
            if file_size_mb > self.log_max_size_mb:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                archive_name = f"{self.log_file_prefix}_{today}_{timestamp}.log"
                archive_path = os.path.join(self.log_directory, archive_name)
                os.rename(self._current_log_file, archive_path)
    
    def _cleanup_old_logs(self):
        """Удаление старых лог-файлов"""
        try:
            for filename in os.listdir(self.log_directory):
                if filename.startswith(self.log_file_prefix) and filename.endswith('.log'):
                    filepath = os.path.join(self.log_directory, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    # Проверяем возраст файла
                    if (datetime.now() - file_time).days > self.log_retention_days:
                        os.remove(filepath)
        except Exception as e:
            self._write_log(LogLevel.ERROR, "Error cleaning up old logs", {"error": str(e)})
    
    def _should_log(self, level: LogLevel) -> bool:
        """Проверяем, нужно ли логировать сообщение данного уровня"""
        level_priority = {
            LogLevel.DEBUG: 1,
            LogLevel.INFO: 2,
            LogLevel.ERROR: 3
        }
        return level_priority[level] >= level_priority[self.log_level]
    
    def _format_message(self, level: LogLevel, message: str, context: Dict[str, Any] = None) -> str:
        """Форматирование сообщения в детализированном формате"""
        timestamp = datetime.now().strftime(self.date_format)
        
        context_str = ""
        if context:
            context_items = []
            for k, v in context.items():
                if isinstance(v, dict) or isinstance(v, list):
                    context_items.append(f"{k}={json.dumps(v, ensure_ascii=False, default=str)}")
                elif isinstance(v, (datetime, date)):
                    context_items.append(f"{k}={v.isoformat()}")
                else:
                    context_items.append(f"{k}={v}")
            context_str = " | " + " | ".join(context_items)
        
        return f"[{timestamp}] [{level.value}] {message}{context_str}"
    
    def _write_log(self, level: LogLevel, message: str, context: Dict[str, Any] = None):
        """Записывает лог в соответствии с настройками"""
        if not self._should_log(level):
            return
        
        formatted_message = self._format_message(level, message, context)
        
        # Проверяем ротацию файла
        today = datetime.now().strftime('%Y-%m-%d')
        if self._current_log_file and today not in self._current_log_file:
            self._rotate_log_file()
        
        # Логируем в консоль
        if self.log_mode in [LogMode.CONSOLE, LogMode.BOTH]:
            print(formatted_message)
        
        # Логируем в файл
        if self.log_mode in [LogMode.FILE, LogMode.BOTH]:
            try:
                if not self._current_log_file:
                    self._rotate_log_file()
                
                with open(self._current_log_file, 'a', encoding='utf-8') as file:
                    file.write(formatted_message + '\n')
                
                # Периодически чистим старые логи
                if datetime.now().hour == 0:  # В полночь
                    self._cleanup_old_logs()
                    
            except Exception as e:
                # Fallback: если не удалось записать в файл, пишем в консоль
                print(f"[ERROR] Ошибка записи в лог-файл: {e}")
    
    def _extract_request_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Извлекает информацию о HTTP запросе из параметров"""
        request_info = {}
        
        # Проверяем наличие request в параметрах
        if 'request' in params and isinstance(params['request'], dict):
            req = params['request']
            request_info = {
                'http_method': req.get('method', ''),
                'http_url': req.get('url', ''),
                'client_ip': req.get('client_ip', '')
            }
        
        return request_info
    
    def handle(self, event: str, params: Dict[str, Any]):
        super().handle(event, params)
        
        # Извлекаем информацию о запросе
        request_info = self._extract_request_info(params)
        
        # Объединяем контекст
        context = {**params}
        if request_info:
            context['request'] = request_info
        
        # Обработка событий системы
        if event == event_type.convert_to_json():
            operation = params.get("operation", "unknown")
            self._write_log(LogLevel.INFO, f"CONVERT_TO_JSON: {operation}", context)
        
        elif event == event_type.reference_added():
            ref_type = params.get("type", "unknown")
            name = params.get("name", "unknown")
            self._write_log(LogLevel.INFO, f"REFERENCE_ADDED: {ref_type} - {name}", context)
        
        elif event == event_type.reference_updated():
            ref_type = params.get("type", "unknown")
            unique_code = params.get("unique_code", "unknown")
            self._write_log(LogLevel.INFO, f"REFERENCE_UPDATED: {ref_type} - {unique_code}", context)
        
        elif event == event_type.reference_deleted():
            ref_type = params.get("type", "unknown")
            unique_code = params.get("unique_code", "unknown")
            self._write_log(LogLevel.WARNING, f"REFERENCE_DELETED: {ref_type} - {unique_code}", context)
        
        elif event == event_type.reference_operation_completed():
            operation = params.get("operation", "unknown")
            status = params.get("status", "unknown")
            
            if status == "success":
                file_path = params.get("file_path", "")
                if file_path:
                    self._write_log(LogLevel.INFO, f"OPERATION_SUCCESS: {operation}", {"file_path": file_path, **context})
                else:
                    self._write_log(LogLevel.INFO, f"OPERATION_SUCCESS: {operation}", context)
            else:
                error = params.get("error", "unknown error")
                self._write_log(LogLevel.ERROR, f"OPERATION_ERROR: {operation}", {"error": error, **context})
        
        elif event == event_type.change_block_period():
            new_block_date = params.get("new_block_date", "unknown")
            if isinstance(new_block_date, (date, datetime)):
                new_block_date = new_block_date.strftime("%Y-%m-%d")
            self._write_log(LogLevel.INFO, f"BLOCK_PERIOD_CHANGED: {new_block_date}", context)
        
        elif event == event_type.add_reference():
            model_type = params.get("model", "unknown")
            self._write_log(LogLevel.INFO, f"ADD_REFERENCE: {model_type}", context)
        
        elif event == event_type.change_reference():
            model_type = params.get("model", {}).get("type", "unknown")
            self._write_log(LogLevel.INFO, f"CHANGE_REFERENCE: {model_type}", context)
        
        elif event == event_type.remove_reference():
            model_type = params.get("model", {}).get("type", "unknown")
            self._write_log(LogLevel.WARNING, f"REMOVE_REFERENCE: {model_type}", context)
        
        elif event == event_type.update_dependencies():
            self._write_log(LogLevel.DEBUG, f"UPDATE_DEPENDENCIES", context)
        
        elif event == event_type.check_dependencies():
            self._write_log(LogLevel.DEBUG, f"CHECK_DEPENDENCIES", context)
        
        elif event == event_type.settings_updated():
            operation = params.get("operation", "unknown")
            status = params.get("status", "unknown")
            
            if status == "success":
                self._write_log(LogLevel.INFO, f"SETTINGS_UPDATED: {operation}", context)
            else:
                error = params.get("error", "unknown error")
                self._write_log(LogLevel.ERROR, f"SETTINGS_UPDATE_ERROR: {operation}", {"error": error, **context})
        
        elif event == "api_request":
            method = params.get("method", "").upper()
            url = params.get("url", "")
            if method in ['DELETE', 'PUT', 'PATCH', 'POST']:
                self._write_log(LogLevel.INFO, f"API_REQUEST: {method} {url}", context)
        
        # Неизвестные события
        else:
            self._write_log(LogLevel.WARNING, f"UNKNOWN_EVENT: {event}", context)
    
    def update_settings(self):
        """Обновляет настройки логирования"""
        self._load_settings()
        self._write_log(LogLevel.INFO, "Logging settings updated")
    
    # Методы для ручного логирования
    def log_debug(self, message: str, context: Dict[str, Any] = None):
        """Ручное логирование отладочного сообщения"""
        self._write_log(LogLevel.DEBUG, message, context)
    
    def log_info(self, message: str, context: Dict[str, Any] = None):
        """Ручное логирование информационного сообщения"""
        self._write_log(LogLevel.INFO, message, context)
    
    def log_error(self, message: str, context: Dict[str, Any] = None):
        """Ручное логирование ошибки"""
        self._write_log(LogLevel.ERROR, message, context)
    
    def log_api_request(self, method: str, url: str, headers: Dict = None, 
                       body: Any = None, params: Dict = None, query: Dict = None,
                       client_ip: str = "", user_agent: str = ""):
        """Логирование HTTP запросов"""
        context = {
            "method": method.upper(),
            "url": url,
            "headers": headers or {},
            "body": body,
            "params": params or {},
            "query": query or {},
            "client_ip": client_ip,
            "user_agent": user_agent
        }
        
        if method.upper() in ['DELETE', 'PUT', 'PATCH', 'POST']:
            self._write_log(LogLevel.INFO, f"API_REQUEST: {method} {url}", context)