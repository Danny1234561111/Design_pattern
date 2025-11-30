from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.core.event_type import event_type
#вместо abstract_logic
class AbstractSubscriber:
    """
    Обработка события
    """
    def handle(self, event: str, params):
        vld.validate(event, str,"event")
        events = event_type.events()
        if event not in events:
            raise OperationException(f"{event} - не является событием! Доступные: {events}")