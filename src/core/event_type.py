"""
Типы событий
"""
class event_type:

    """
    Событие - смена даты блокировки
    """
    @staticmethod
    def change_block_period() -> str:
        return "change_block_period"
    
    """
    Событие - сформирован Json
    """
    @staticmethod
    def convert_to_json() -> str:
        return "convert_to_json"

    """
    Событие - добавление reference
    """
    @staticmethod
    def add_reference() -> str:
        return "add_reference"

    """
    Событие - изменение reference
    """
    @staticmethod
    def change_reference() -> str:
        return "change_reference"

    """
    Событие - удаление reference
    """
    @staticmethod
    def remove_reference() -> str:
        return "remove_reference"

    """
    Событие - обновить зависимости от reference
    """
    @staticmethod
    def update_dependencies() -> str:
        return "update_dependencies"

    """
    Событие - проверить зависимости от reference
    """
    @staticmethod
    def check_dependencies() -> str:
        return "check_dependencies"

    """
    Событие - reference добавлен
    """
    @staticmethod
    def reference_added() -> str:
        return "reference_added"

    """
    Событие - reference обновлен
    """
    @staticmethod
    def reference_updated() -> str:
        return "reference_updated"

    """
    Событие - reference удален
    """
    @staticmethod
    def reference_deleted() -> str:
        return "reference_deleted"

    """
    Событие - операция с reference завершена
    """
    @staticmethod
    def reference_operation_completed() -> str:
        return "reference_operation_completed"

    """
    Получить список всех событий
    """
    @staticmethod
    def events() -> list:
        result = []
        methods = [method for method in dir(event_type) if
                    callable(getattr(event_type, method)) and not method.startswith('__') and method != "events"]
        for method in methods:
            key = getattr(event_type, method)()
            result.append(key)

        return result