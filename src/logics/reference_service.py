# src/services/reference_service.py
from src.core.abstract_subscriber import AbstractSubscriber
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.logics.factory_converters import FactoryConverters

# Импорт логгера
from src.logics.print_service import print_service


class ReferenceService(AbstractSubscriber):
    def __init__(self):
        super().__init__()
        observe_service.add(self)
        # Инициализация логгера
        self._logger = print_service()

    @staticmethod
    def add(reference_type: str, properties: dict):
        """Добавление нового элемента справочника"""
        vld.validate(reference_type, str, "reference_type")
        vld.validate(properties, dict, "properties")
        
        # Логируем добавление
        logger = print_service()
        logger.log_info(f"Adding reference: {reference_type}", {
            "name": properties.get('name', 'unknown'),
            "properties": properties
        })
        
        observe_service.create_event(event_type.add_reference(), {
            "model": reference_type,
            "properties": properties
        })

    @staticmethod
    def change(reference_type: str, properties: dict):
        """Изменение элемента справочника"""
        vld.validate(reference_type, str, "reference_type")
        vld.validate(properties, dict, "properties")
        
        if "unique_code" not in properties:
            error_msg = "Отсутствует необходимое поле unique_code"
            logger = print_service()
            logger.log_error(error_msg, {"properties": properties})
            raise OperationException(error_msg)
        
        # Логируем изменение
        logger = print_service()
        logger.log_info(f"Changing reference: {reference_type}", {
            "unique_code": properties["unique_code"],
            "properties": properties
        })
        
        observe_service.create_event(event_type.change_reference(), {
            "model": {
                "type": reference_type,
                "unique_code": properties["unique_code"]
            },
            "properties": properties
        })

    @staticmethod
    def remove(reference_type: str, properties: dict):
        """Удаление элемента справочника"""
        vld.validate(reference_type, str, "reference_type")
        vld.validate(properties, dict, "properties")
        
        if "unique_code" not in properties:
            error_msg = "Отсутствует необходимое поле unique_code"
            logger = print_service()
            logger.log_error(error_msg, {"properties": properties})
            raise OperationException(error_msg)
        
        # Логируем удаление
        logger = print_service()
        logger.log_warning(f"Removing reference: {reference_type}", {
            "unique_code": properties["unique_code"]
        })
        
        observe_service.create_event(event_type.remove_reference(), {
            "model": {
                "type": reference_type,
                "unique_code": properties["unique_code"]
            },
            "properties": properties
        })

    def get(self, reference_type: str, name: str):
        """Получение элемента справочника по имени"""
        try:
            self._logger.log_debug(f"Getting reference: type={reference_type}, name={name}")
            
            # Реализация метода get (должна быть в вашем коде)
            # Возвращает элемент справочника по имени
            
            self._logger.log_debug(f"Reference retrieved: type={reference_type}, name={name}")
            return {"unique_code": "placeholder", "name": name}  # Заглушка
        except Exception as e:
            self._logger.log_error(f"Error getting reference: {str(e)}", {
                "reference_type": reference_type,
                "name": name
            })
            raise

    def handle(self, event: str, params: dict):
        """Обработка событий"""
        super().handle(event, params)
        
        # Логируем события, связанные со справочниками
        if event == event_type.reference_added():
            ref_type = params.get("type", "unknown")
            name = params.get("name", "unknown")
            self._logger.log_info(f"Reference added event handled: {ref_type} - {name}", params)
        
        elif event == event_type.reference_updated():
            ref_type = params.get("type", "unknown")
            unique_code = params.get("unique_code", "unknown")
            self._logger.log_info(f"Reference updated event handled: {ref_type} - {unique_code}", params)
        
        elif event == event_type.reference_deleted():
            ref_type = params.get("type", "unknown")
            unique_code = params.get("unique_code", "unknown")
            self._logger.log_warning(f"Reference deleted event handled: {ref_type} - {unique_code}", params)
        
        elif event == event_type.reference_operation_completed():
            operation = params.get("operation", "unknown")
            status = params.get("status", "unknown")
            
            if status == "success":
                self._logger.log_info(f"Reference operation completed: {operation}", params)
            else:
                error = params.get("error", "unknown error")
                self._logger.log_error(f"Reference operation failed: {operation}", {
                    "error": error,
                    **params
                })