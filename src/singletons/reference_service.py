from typing import Dict, List, Optional, Any
from datetime import datetime
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.logics.factory_converters import FactoryConverters
from src.core.event_type import event_type
from src.core.observe_service import observe_service
from src.logics.reference_observer import UsageCheckObserver, RecalculationObserver

class ReferenceService:
    """Сервис для работы со справочниками"""
    
    def __init__(self):
        self.repository = Repository()
        self.factory_converters = FactoryConverters()
        self.observers: List[ReferenceObserver] = []
        self._initialize_observers()
    
    def _initialize_observers(self):
        """Инициализация бизнес-наблюдателей"""
        self.observers.extend([
            UsageCheckObserver(),
            RecalculationObserver(),
            # SettingsObserver()  # Раскомментировать когда SettingsManager будет доступен
        ])
    
    def _get_repository_key(self, reference_type: str) -> str:
        """Получение ключа репозитория по типу справочника"""
        keys = {
            "nomenclatures": Repository.nomenclatures_key,
            "measure_units": Repository.measure_unit_key,
            "nomenclature_groups": Repository.nomenclature_group_key,
            "storages": Repository.storages_key
        }
        return keys.get(reference_type, reference_type)
    
    def _create_event_data(self, reference_type: str, name: str, data: Dict[str, Any] = None, 
                          operation: str = "") -> Dict[str, Any]:
        """Создает данные для события"""
        event_data = {
            "reference_type": reference_type,
            "name": name,
            "operation": operation,
            "timestamp": self._get_current_timestamp()
        }
        if data:
            event_data["data"] = data
        return event_data
    
    def _get_current_timestamp(self) -> str:
        """Возвращает текущую метку времени"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def find_by_criteria(self, reference_type: str, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Поиск элементов по критериям"""
        vld.is_str(reference_type, "reference_type")
        vld.is_dict(criteria, "criteria")
        
        repo_key = self._get_repository_key(reference_type)
        if repo_key not in self.repository.data:
            raise OperationException(f"Неизвестный тип справочника: {reference_type}")
        
        items_dict = self.repository.data[repo_key]
        results = []
        
        # Простой поиск по имени (основной случай)
        if "name" in criteria:
            name = criteria["name"]
            item = self._find_item_by_name(items_dict, name)
            if item:
                results.append(item)
        
        # Если нужен более сложный поиск, используем простую фильтрацию
        elif len(criteria) > 0:
            for item in items_dict.values():
                matches = True
                for field, value in criteria.items():
                    item_value = getattr(item, field, None)
                    # Если значение - объект, сравниваем по имени
                    if hasattr(item_value, 'name'):
                        item_value = item_value.name
                    if item_value != value:
                        matches = False
                        break
                if matches:
                    results.append(item)
        else:
            # Если критериев нет, возвращаем все элементы
            results = list(items_dict.values())
        
        # Создаем событие о завершении операции поиска
        event_data = self._create_event_data(
            reference_type=reference_type,
            name="search_operation",
            data={"criteria": criteria, "results_count": len(results)},
            operation="search"
        )
        observe_service.create_event(
            event_type.reference_operation_completed(), 
            event_data
        )
        
        return [self._model_to_dict(item) for item in results]
    
    def _find_item_by_name(self, items_dict: Dict, name: str):
        """Находит элемент по имени в словаре"""
        # Прямой поиск по ключу
        if name in items_dict:
            return items_dict[name]
        
        # Поиск по атрибуту name
        for item in items_dict.values():
            if hasattr(item, 'name') and item.name == name:
                return item
            # Дополнительная проверка: если имя в нижнем регистре
            if hasattr(item, 'name') and item.name.lower() == name.lower():
                return item
        
        return None
    
    def get(self, reference_type: str, name: str) -> Optional[Dict[str, Any]]:
        """Получение элемента по имени"""
        vld.is_str(reference_type, "reference_type")
        vld.is_str(name, "name")
        
        repo_key = self._get_repository_key(reference_type)
        if repo_key not in self.repository.data:
            raise OperationException(f"Неизвестный тип справочника: {reference_type}")
        
        items_dict = self.repository.data[repo_key]
        item = self._find_item_by_name(items_dict, name)
        
        if item:
            return self._model_to_dict(item)
        return None
    
    def get_all(self, reference_type: str) -> List[Dict[str, Any]]:
        """Получение всех элементов справочника"""
        repo_key = self._get_repository_key(reference_type)
        if repo_key not in self.repository.data:
            raise OperationException(f"Неизвестный тип справочника: {reference_type}")
        
        items_dict = self.repository.data[repo_key]
        
        # Создаем событие о получении всех элементов
        event_data = self._create_event_data(
            reference_type=reference_type,
            name="get_all_operation",
            data={"items_count": len(items_dict)},
            operation="get_all"
        )
        observe_service.create_event(
            event_type.reference_operation_completed(), 
            event_data
        )
        
        return [self._model_to_dict(item) for item in items_dict.values()]
    
    def add(self, reference_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Добавление нового элемента"""
        vld.is_str(reference_type, "reference_type")
        vld.is_dict(data, "data")
        
        if "name" not in data:
            raise OperationException("Поле 'name' обязательно для добавления")
        
        # Проверка существования
        existing = self.get(reference_type, data["name"])
        if existing:
            raise OperationException(f"Элемент с именем '{data['name']}' уже существует")
        
        # Создание и сохранение элемента
        new_item = self._create_model(reference_type, data)
        repo_key = self._get_repository_key(reference_type)
        
        # Сохраняем в репозиторий
        self.repository.data[repo_key][data["name"]] = new_item
        
        result = self._model_to_dict(new_item)
        
        # Создаем событие о добавлении
        event_data = self._create_event_data(
            reference_type=reference_type,
            name=data["name"],
            data=result,
            operation="add"
        )
        observe_service.create_event(
            event_type.reference_added(), 
            event_data
        )
        
        return result
    
    def update(self, reference_type: str, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление элемента"""
        vld.is_str(reference_type, "reference_type")
        vld.is_str(name, "name")
        vld.is_dict(data, "data")
        
        # Находим элемент
        current_item = self._get_model(reference_type, name)
        if not current_item:
            raise OperationException(f"Элемент '{name}' не найден")
        
        # Сохраняем старые данные для события
        old_data = self._model_to_dict(current_item)
        
        # Обновляем данные
        for key, value in data.items():
            if hasattr(current_item, key):
                # Если обновляем имя, нужно изменить ключ в словаре
                if key == 'name' and value != name:
                    self._update_item_name(reference_type, name, value, current_item)
                else:
                    setattr(current_item, key, value)
        
        result = self._model_to_dict(current_item)
        
        # Уведомляем бизнес-наблюдателей
        for observer in self.observers:
            observer.on_after_update(reference_type, name, data)
        
        # Создаем событие об обновлении
        event_data = self._create_event_data(
            reference_type=reference_type,
            name=name,
            data={
                "old_data": old_data,
                "new_data": result,
                "changes": data
            },
            operation="update"
        )
        observe_service.create_event(
            event_type.reference_updated(), 
            event_data
        )
        
        return result
    
    def _update_item_name(self, reference_type: str, old_name: str, new_name: str, item: Any):
        """Обновляет имя элемента и меняет ключ в словаре"""
        repo_key = self._get_repository_key(reference_type)
        
        # Удаляем старый ключ
        if old_name in self.repository.data[repo_key]:
            del self.repository.data[repo_key][old_name]
        
        # Устанавливаем новое имя и добавляем с новым ключом
        setattr(item, 'name', new_name)
        self.repository.data[repo_key][new_name] = item
    
    def delete(self, reference_type: str, name: str) -> bool:
        """Удаление элемента"""
        vld.is_str(reference_type, "reference_type")
        vld.is_str(name, "name")
        
        repo_key = self._get_repository_key(reference_type)
        if repo_key not in self.repository.data:
            raise OperationException(f"Неизвестный тип справочника: {reference_type}")
        
        # Проверяем существование
        item = self._find_item_by_name(self.repository.data[repo_key], name)
        if not item:
            raise OperationException(f"Элемент '{name}' не найден")
        
        # Сохраняем данные для события
        deleted_data = self._model_to_dict(item)
        
        # Уведомляем бизнес-наблюдателей перед удалением
        for observer in self.observers:
            observer.on_before_delete(reference_type, name)
        
        # Находим точное имя для удаления (может отличаться от переданного)
        exact_name = name
        if name not in self.repository.data[repo_key]:
            for key, value in self.repository.data[repo_key].items():
                if hasattr(value, 'name') and value.name == name:
                    exact_name = key
                    break
        
        # Удаляем из репозитория
        if exact_name in self.repository.data[repo_key]:
            del self.repository.data[repo_key][exact_name]
        
        # Создаем событие об удалении
        event_data = self._create_event_data(
            reference_type=reference_type,
            name=name,
            data=deleted_data,
            operation="delete"
        )
        observe_service.create_event(
            event_type.reference_deleted(), 
            event_data
        )
        
        return True
    
    def _get_model(self, reference_type: str, name: str):
        """Получает модель по имени"""
        repo_key = self._get_repository_key(reference_type)
        if repo_key not in self.repository.data:
            return None
        
        return self._find_item_by_name(self.repository.data[repo_key], name)
    
    def _model_to_dict(self, model) -> Dict[str, Any]:
        """Конвертирует модель в словарь"""
        try:
            # Пробуем использовать factory_converters
            result = self.factory_converters.convert(model)
            # Убедимся, что это словарь
            if isinstance(result, dict):
                return result
            else:
                # Если вернулся список или другой тип, оборачиваем в словарь
                return {"data": result}
        except Exception as e:
            # Fallback: ручная конвертация
            return self._manual_model_to_dict(model)
    
    def _manual_model_to_dict(self, model) -> Dict[str, Any]:
        """Ручная конвертация модели в словарь"""
        result = {}
        if hasattr(model, '__dict__'):
            for key, value in model.__dict__.items():
                if not key.startswith('_'):
                    # Обрабатываем вложенные объекты
                    if hasattr(value, 'name'):
                        result[key] = value.name
                    elif hasattr(value, '__dict__'):
                        # Рекурсивно конвертируем вложенные объекты
                        result[key] = self._manual_model_to_dict(value)
                    else:
                        result[key] = value
        else:
            # Если нет __dict__, пытаемся получить атрибуты
            for attr in dir(model):
                if not attr.startswith('_') and not callable(getattr(model, attr)):
                    value = getattr(model, attr)
                    if hasattr(value, 'name'):
                        result[attr] = value.name
                    else:
                        result[attr] = value
        return result
    
    def _create_model(self, reference_type: str, data: Dict[str, Any]):
        """Создает модель из данных (упрощенная реализация)"""
        # Для тестирования используем простой объект
        # В реальном проекте нужно создавать конкретные модели
        class SimpleModel:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        return SimpleModel(**data)
    
    def add_observer(self, observer):
        """Добавление наблюдателя"""
        from src.services.reference_observer import ReferenceObserver
        if isinstance(observer, ReferenceObserver):
            self.observers.append(observer)
    
    def debug_repository(self):
        """Метод для отладки - показывает содержимое репозитория"""
        debug_info = {}
        for key in Repository.keys():
            if key in self.repository.data:
                items = self.repository.data[key]
                names = []
                for item_key, item in items.items():
                    if hasattr(item, 'name'):
                        names.append(f"{item_key} (name: {item.name})")
                    else:
                        names.append(str(item_key))
                
                debug_info[key] = {
                    'count': len(items),
                    'items': names
                }
        return debug_info