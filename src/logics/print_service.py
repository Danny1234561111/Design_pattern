from src.core.abstract_logic import abstract_logic
from src.core.observe_service import observe_service
from src.core.event_type import event_type

class print_service(abstract_logic):

    def __init__(self):
        super().__init__()

        # Подключение в наблюдение
        observe_service.add(self)

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  

        if event == event_type.convert_to_json():
            print(f"params:{ params } ")
        
        elif event == event_type.reference_added():
            print(f"[REFERENCE_ADDED] Добавлен новый элемент: {params}")
        
        elif event == event_type.reference_updated():
            print(f"[REFERENCE_UPDATED] Обновлен элемент: {params}")
        
        elif event == event_type.reference_deleted():
            print(f"[REFERENCE_DELETED] Удален элемент: {params}")
        
        elif event == event_type.reference_operation_completed():
            print(f"[REFERENCE_OPERATION] Операция завершена: {params}")
        
        elif event == event_type.change_block_period():
            print(f"[BLOCK_PERIOD_CHANGED] Изменена дата блокировки: {params}")