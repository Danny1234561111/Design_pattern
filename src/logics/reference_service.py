# src/services/reference_service.py
from src.core.abstract_subscriber import AbstractSubscriber
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.logics.factory_converters import FactoryConverters


class ReferenceService(AbstractSubscriber):
    def __init__(self):
        super().__init__()
        observe_service.add(self)

    @staticmethod
    def add(reference_type: str, properties: dict):
        vld.validate(reference_type, str, "reference_type")
        vld.validate(properties, dict, "properties")
        observe_service.create_event(event_type.add_reference(), {
            "model": reference_type,
            "properties": properties
        })

    @staticmethod
    def change(reference_type: str, properties: dict):
        vld.validate(reference_type, str, "reference_type")
        vld.validate(properties, dict, "properties")
        if "unique_code" not in properties:
            raise OperationException("Отсутствует необходимое поле unique_code")
        
        observe_service.create_event(event_type.change_reference(), {
            "model": {
                "type": reference_type,
                "unique_code": properties["unique_code"]
            },
            "properties": properties
        })

    @staticmethod
    def remove(reference_type: str, properties: dict):
        vld.validate(reference_type, str, "reference_type")
        vld.validate(properties, dict, "properties")
        if "unique_code" not in properties:
            raise OperationException("Отсутствует необходимое поле unique_code")
        
        observe_service.create_event(event_type.remove_reference(), {
            "model": {
                "type": reference_type,
                "unique_code": properties["unique_code"]
            },
            "properties": properties
        })