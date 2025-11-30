
from src.core.abstract_logic import abstract_logic
from src.core.observe_service import observe_service
from src.core.event_type import event_type
import os
from datetime import datetime

class print_service(abstract_logic):

    def __init__(self):
        super().__init__()
        self.__log_file = "app.log"
        
        # Создаем директорию для логов если не существует
        log_dir = os.path.dirname(self.__log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        # Подключение в наблюдение
        observe_service.add(self)

    def __write_to_log(self, message: str):
        """Записывает сообщение в лог-файл"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            
            with open(self.__log_file, 'a', encoding='utf-8') as file:
                file.write(log_message)
                
        except Exception as e:
            # Если не удалось записать в лог, выводим в консоль как запасной вариант
            print(f"Ошибка записи в лог: {e}")

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  

        if event == event_type.convert_to_json():
            self.__write_to_log(f"CONVERT_TO_JSON: params: {params}")
        
        elif event == event_type.reference_added():
            ref_type = params.get("type", "unknown")
            name = params.get("name", "unknown")
            self.__write_to_log(f"REFERENCE_ADDED: Добавлен новый элемент типа '{ref_type}': {name}")
        
        elif event == event_type.reference_updated():
            ref_type = params.get("type", "unknown")
            unique_code = params.get("unique_code", "unknown")
            self.__write_to_log(f"REFERENCE_UPDATED: Обновлен элемент типа '{ref_type}' с кодом: {unique_code}")
        
        elif event == event_type.reference_deleted():
            ref_type = params.get("type", "unknown")
            unique_code = params.get("unique_code", "unknown")
            self.__write_to_log(f"REFERENCE_DELETED: Удален элемент типа '{ref_type}' с кодом: {unique_code}")
        
        elif event == event_type.reference_operation_completed():
            operation = params.get("operation", "unknown")
            status = params.get("status", "unknown")
            
            if status == "success":
                file_path = params.get("file_path", "")
                if file_path:
                    self.__write_to_log(f"OPERATION_SUCCESS: Операция '{operation}' завершена успешно. Файл: {file_path}")
                else:
                    self.__write_to_log(f"OPERATION_SUCCESS: Операция '{operation}' завершена успешно")
            else:
                error = params.get("error", "unknown error")
                self.__write_to_log(f"OPERATION_ERROR: Ошибка операции '{operation}': {error}")
        
        elif event == event_type.change_block_period():
            new_block_date = params.get("new_block_date", "unknown")
            self.__write_to_log(f"BLOCK_PERIOD_CHANGED: Изменена дата блокировки на: {new_block_date}")
        
        elif event == event_type.add_reference():
            self.__write_to_log(f"ADD_REFERENCE: Добавление reference: {params}")
        
        elif event == event_type.change_reference():
            self.__write_to_log(f"CHANGE_REFERENCE: Изменение reference: {params}")
        
        elif event == event_type.remove_reference():
            self.__write_to_log(f"REMOVE_REFERENCE: Удаление reference: {params}")