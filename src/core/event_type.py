"""
Типы событий системы
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
    Событие - обновлены настройки
    """
    @staticmethod
    def settings_updated() -> str:
        return "settings_updated"

    """
    Событие - складская операция
    """
    @staticmethod
    def storage_operation() -> str:
        return "storage_operation"

    """
    Событие - складская операция создана
    """
    @staticmethod
    def storage_operation_created() -> str:
        return "storage_operation_created"

    """
    Событие - складская операция обновлена
    """
    @staticmethod
    def storage_operation_updated() -> str:
        return "storage_operation_updated"

    """
    Событие - складская операция удалена
    """
    @staticmethod
    def storage_operation_deleted() -> str:
        return "storage_operation_deleted"

    """
    Событие - расчет остатков (OST)
    """
    @staticmethod
    def ost_calculation() -> str:
        return "ost_calculation"

    """
    Событие - расчет остатков завершен
    """
    @staticmethod
    def ost_calculation_completed() -> str:
        return "ost_calculation_completed"

    """
    Событие - ошибка расчета остатков
    """
    @staticmethod
    def ost_calculation_error() -> str:
        return "ost_calculation_error"

    """
    Событие - запуск приложения
    """
    @staticmethod
    def application_started() -> str:
        return "application_started"

    """
    Событие - остановка приложения
    """
    @staticmethod
    def application_stopped() -> str:
        return "application_stopped"

    """
    Событие - ошибка приложения
    """
    @staticmethod
    def application_error() -> str:
        return "application_error"

    """
    Событие - API запрос
    """
    @staticmethod
    def api_request() -> str:
        return "api_request"

    """
    Событие - API запрос успешен
    """
    @staticmethod
    def api_request_success() -> str:
        return "api_request_success"

    """
    Событие - API запрос с ошибкой
    """
    @staticmethod
    def api_request_error() -> str:
        return "api_request_error"

    """
    Событие - аутентификация пользователя
    """
    @staticmethod
    def user_authenticated() -> str:
        return "user_authenticated"

    """
    Событие - ошибка аутентификации
    """
    @staticmethod
    def authentication_error() -> str:
        return "authentication_error"

    """
    Событие - выход пользователя
    """
    @staticmethod
    def user_logged_out() -> str:
        return "user_logged_out"

    """
    Событие - экспорт данных
    """
    @staticmethod
    def data_export() -> str:
        return "data_export"

    """
    Событие - импорт данных
    """
    @staticmethod
    def data_import() -> str:
        return "data_import"

    """
    Событие - отчет сгенерирован
    """
    @staticmethod
    def report_generated() -> str:
        return "report_generated"

    """
    Событие - запуск фоновой задачи
    """
    @staticmethod
    def background_task_started() -> str:
        return "background_task_started"

    """
    Событие - завершение фоновой задачи
    """
    @staticmethod
    def background_task_completed() -> str:
        return "background_task_completed"

    """
    Событие - ошибка фоновой задачи
    """
    @staticmethod
    def background_task_error() -> str:
        return "background_task_error"

    """
    Событие - кэш обновлен
    """
    @staticmethod
    def cache_updated() -> str:
        return "cache_updated"

    """
    Событие - кэш очищен
    """
    @staticmethod
    def cache_cleared() -> str:
        return "cache_cleared"

    """
    Событие - уведомление пользователя
    """
    @staticmethod
    def user_notification() -> str:
        return "user_notification"

    """
    Событие - системное предупреждение
    """
    @staticmethod
    def system_warning() -> str:
        return "system_warning"

    """
    Событие - критическая ошибка
    """
    @staticmethod
    def critical_error() -> str:
        return "critical_error"

    """
    Событие - проверка целостности данных
    """
    @staticmethod
    def data_integrity_check() -> str:
        return "data_integrity_check"

    """
    Событие - резервное копирование данных
    """
    @staticmethod
    def data_backup() -> str:
        return "data_backup"

    """
    Событие - восстановление данных
    """
    @staticmethod
    def data_restore() -> str:
        return "data_restore"

    """
    Событие - аудит безопасности
    """
    @staticmethod
    def security_audit() -> str:
        return "security_audit"

    """
    Получить список всех событий
    """
    @staticmethod
    def events() -> list:
        result = []
        methods = [method for method in dir(event_type) if
                    callable(getattr(event_type, method)) and 
                    not method.startswith('__') and 
                    method != "events" and
                    method != "get_events_by_category"]  # Исключаем метод с параметрами
        for method in methods:
            key = getattr(event_type, method)()
            result.append(key)

        return result
    
    """
    Получить события по категории
    """
    @staticmethod
    def get_events_by_category(category: str) -> list:
        """Возвращает события по категории:
        - reference: события справочников
        - storage: события складских операций
        - system: системные события
        - security: события безопасности
        - data: события работы с данными
        - api: события API
        """
        categories = {
            "reference": [
                event_type.add_reference(),
                event_type.change_reference(),
                event_type.remove_reference(),
                event_type.reference_added(),
                event_type.reference_updated(),
                event_type.reference_deleted(),
                event_type.reference_operation_completed(),
                event_type.update_dependencies(),
                event_type.check_dependencies()
            ],
            "storage": [
                event_type.storage_operation(),
                event_type.storage_operation_created(),
                event_type.storage_operation_updated(),
                event_type.storage_operation_deleted(),
                event_type.ost_calculation(),
                event_type.ost_calculation_completed(),
                event_type.ost_calculation_error()
            ],
            "system": [
                event_type.application_started(),
                event_type.application_stopped(),
                event_type.application_error(),
                event_type.settings_updated(),
                event_type.system_warning(),
                event_type.critical_error(),
                event_type.change_block_period(),
                event_type.convert_to_json()
            ],
            "security": [
                event_type.user_authenticated(),
                event_type.authentication_error(),
                event_type.user_logged_out(),
                event_type.security_audit()
            ],
            "data": [
                event_type.data_export(),
                event_type.data_import(),
                event_type.data_backup(),
                event_type.data_restore(),
                event_type.data_integrity_check(),
                event_type.cache_updated(),
                event_type.cache_cleared()
            ],
            "api": [
                event_type.api_request(),
                event_type.api_request_success(),
                event_type.api_request_error()
            ],
            "tasks": [
                event_type.background_task_started(),
                event_type.background_task_completed(),
                event_type.background_task_error()
            ],
            "reports": [
                event_type.report_generated()
            ],
            "notifications": [
                event_type.user_notification()
            ]
        }
        
        return categories.get(category, [])