from abc import ABC
import uuid
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.core.abstract_subscriber import AbstractSubscriber
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.utils import get_fields

class abstract_reference(ABC, AbstractSubscriber):
    # Уникальный ID модели
    __unique_code: str

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex
        observe_service.add(self)

    # Уникальный код
    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        vld.validate(value, str)
        self.__unique_code = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, abstract_reference):
            return False
        return self.unique_code == other.unique_code

    def __lt__(self, other) -> bool:
        if not isinstance(other, abstract_reference):
            return False
        return self.unique_code < other.unique_code

    def __hash__(self) -> int:
        return hash(self.unique_code)

    def __contains__(self, value) -> bool:
        values = [getattr(self, field) for field in get_fields(self)]
        return any(value == item or (isinstance(item, (list, tuple, abstract_reference, str)) and value in item) for item in values)

    def __str__(self):
        return self.unique_code

    """
    Обработка событий
    """
    def handle(self, event: str, params: dict):
        vld.validate(params, dict)
        super().handle(event, params)

        if event == event_type.update_dependencies():
            old_model = params["old_model"]
            new_model = params["new_model"]
            vld.validate(old_model, abstract_reference)
            vld.validate(new_model, abstract_reference)
            for field in get_fields(self):
                if getattr(self, field) == old_model:
                    setattr(self, field, new_model)
        elif event == event_type.check_dependencies():
            model = params["model"]
            vld.validate(model, abstract_reference)
            for field in get_fields(self):
                if getattr(self, field) == model:
                    raise OperationException(f"Отказ в удалении объекта по причине: удаляемый объект содержится в {self}.")