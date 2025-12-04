import json
import os
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.core.abstract_subscriber import AbstractSubscriber
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.core.abstract_dto import object_to_dto
from src.singletons.repository import Repository
from src.singletons.settings_manager import SettingsManager
from src.logics.factory_converters import FactoryConverters

# Импорты для конвертации моделей
from src.dtos.measure_unit_dto import MeasureUnitDto
from src.dtos.nomenclature_dto import NomenclatureDto
from src.dtos.nomenclature_group_dto import NomenclatureGroupDto
from src.dtos.recipe_dto import RecipeDto
from src.dtos.transaction_dto import TransactionDto
from src.dtos.storage_dto import StorageDto
from src.models.recipe_model import RecipeModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.transaction_model import TransactionModel
from src.models.storage_model import StorageModel

# Импорт логгера
from src.logics.print_service import print_service


class StartService(AbstractSubscriber):
    __instance = None
    __file_name: str = ""
    __repository: Optional[Repository] = Repository()
    __settings_manager: SettingsManager = SettingsManager()

    # Соответствие типов справочников DTO и моделям
    __reference_mapping = {
        "nomenclatures": (NomenclatureDto, NomenclatureModel),
        "measure_units": (MeasureUnitDto, MeasureUnitModel),
        "nomenclature_groups": (NomenclatureGroupDto, NomenclatureGroupModel),
        "storages": (StorageDto, StorageModel),
        "transactions": (TransactionDto, TransactionModel),
        "recipes": (RecipeDto, RecipeModel)
    }

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self.__repository.initalize()
        observe_service.add(self)
        
        # Инициализируем логгер
        self._logger = print_service()

    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = vld.is_file_exists(value)

    @property
    def data(self) -> dict:
        return self.__repository.data
    
    @property
    def block_date(self) -> date:
        return self.__settings_manager.settings.block_date
    
    @block_date.setter
    def block_date(self, value: date):
        vld.validate(value, date, "block_date")
        self.__settings_manager.settings.block_date = value

    @property
    def repository(self) -> Repository:
        return self.__repository

    @property
    def nomenclature_groups(self) -> Dict[str, NomenclatureGroupModel]:
        return self.data[Repository.nomenclature_group_key]
    
    @property
    def measure_units(self) -> Dict[str, MeasureUnitModel]:
        return self.data[Repository.measure_unit_key]
    
    @property
    def nomenclatures(self) -> Dict[str, NomenclatureModel]:
        return self.data[Repository.nomenclatures_key]
    
    @property
    def storages(self) -> Dict[str, StorageModel]:
        return self.data[Repository.storages_key]
    
    @property
    def transactions(self) -> Dict[str, TransactionModel]:
        return self.data[Repository.transactions_key]
    
    @property
    def recipes(self) -> Dict[str, RecipeModel]:
        return self.data[Repository.recipes_key]
    
    @property
    def settings_manager(self) -> SettingsManager:
        return self.__settings_manager

    def load(self) -> bool:
        self.__repository.initalize()
        if not self.file_name:
            raise OperationException("Data can't be loaded, file_name field is empty")
        
        try:
            # Создаем событие о начале загрузки
            observe_service.create_event(event_type.convert_to_json(), {
                "file": self.file_name,
                "operation": "start_loading"
            })
            
            # Загружаем настройки
            self.__settings_manager.load(self.file_name)
            
            # Логируем загрузку настроек
            self._logger.log_info(f"Settings loaded from {self.file_name}", {
                "block_date": self.block_date,
                "log_level": self.__settings_manager.settings.log_level
            })
            
            # Загружаем данные моделей
            with open(self.file_name, mode='r', encoding="utf-8") as file:
                objects = json.load(file)
                data = objects.get("models", {})
                block_date = None
                if "block_date" in objects:
                    block_date = datetime.strptime(objects["block_date"], "%Y-%m-%d").date()
                
                # Логируем загрузку данных
                model_counts = {}
                for key in ["nomenclature_groups", "measure_units", "nomenlatures", 
                           "recipes", "storages", "transactions"]:
                    if key in data:
                        model_counts[key] = len(data[key])
                
                self._logger.log_info("Loading models from file", {
                    "file": self.file_name,
                    "model_counts": model_counts,
                    "block_date": block_date
                })
                
                result = self.convert(data, block_date)
                
                # Логируем успешную загрузку
                self._logger.log_info("Data loaded successfully", {
                    "total_models": sum(len(v) for v in self.__repository.data.values())
                })
                
                return result
                
        except json.JSONDecodeError as e:
            # Создаем событие об ошибке
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "load_data",
                "status": "error",
                "error": f"Invalid JSON file: {e}"
            })
            self._logger.log_error("Invalid JSON file", {
                "file": self.file_name,
                "error": str(e)
            })
            raise OperationException(f"Invalid JSON file: {e}")
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "load_data",
                "status": "error",
                "error": f"Error loading data: {e}"
            })
            self._logger.log_error("Error loading data", {
                "file": self.file_name,
                "error": str(e)
            })
            raise OperationException(f"Error loading data: {e}")

    def __get_ost_file_name(self) -> str:
        """Генерирует имя файла для остатков на основе основного файла"""
        base_name = self.file_name.replace('.json', '')
        return f"{base_name}_ost.json"
    
    def save_repository_data(self):
        """Сохраняет данные репозитория в отдельный файл для остатков"""
        ost_file_name = self.__get_ost_file_name()
        
        repository_data = self.__get_repository_data()
        
        # Сериализуем данные безопасно
        def default_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)
        
        try:
            with open(ost_file_name, mode='w', encoding="utf-8") as file:
                json.dump(repository_data, file, ensure_ascii=False, indent=2, default=default_serializer)
            
            self._logger.log_info("Repository data saved", {
                "file": ost_file_name,
                "headers_count": len(repository_data.get("headers", [])),
                "transactions_count": len(repository_data.get("next_transactions", []))
            })
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_repository_data",
                "status": "error",
                "error": f"Failed to save repository data: {e}"
            })
            self._logger.log_error("Failed to save repository data", {
                "file": ost_file_name,
                "error": str(e)
            })
            raise OperationException(f"Failed to save repository data: {e}")

    def load_repository_data(self) -> bool:
        """Загружает данные репозитория из файла остатков"""
        ost_file_name = self.__get_ost_file_name()
        
        try:
            with open(ost_file_name, mode='r', encoding="utf-8") as file:
                repo_data = json.load(file)
                self.__load_repository_data(repo_data)
                
                self._logger.log_info("Repository data loaded", {
                    "file": ost_file_name,
                    "headers_count": len(repo_data.get("headers", [])),
                    "transactions_count": len(repo_data.get("next_transactions", []))
                })
                
                return True
        except FileNotFoundError:
            self._logger.log_debug("OST file not found", {"file": ost_file_name})
            return False
        except json.JSONDecodeError as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "load_repository_data",
                "status": "error", 
                "error": f"Invalid OST JSON file: {e}"
            })
            self._logger.log_error("Invalid OST JSON file", {
                "file": ost_file_name,
                "error": str(e)
            })
            raise OperationException(f"Invalid OST JSON file: {e}")

    def __get_repository_data(self) -> dict:
        return {
            "headers": self.repository.headers,
            "turnovers_history": self.repository.turnovers_history,
            "next_transactions": [str(txn) for txn in self.repository.next_transactions],
            "display_data_dict": self.repository.display_data_dict,
            "block_date": self.repository.block_date.isoformat() if self.repository.block_date else None
        }

    def __load_repository_data(self, repo_data: dict):
        if "headers" in repo_data:
            self.repository.headers = repo_data["headers"]
        if "turnovers_history" in repo_data:
            self.repository.turnovers_history = repo_data["turnovers_history"]
        if "next_transactions" in repo_data:
            self.repository.next_transactions = repo_data["next_transactions"]
        if "display_data_dict" in repo_data:
            self.repository.display_data_dict = repo_data["display_data_dict"]
        if "block_date" in repo_data and repo_data["block_date"]:
            self.repository.block_date = datetime.strptime(
                repo_data["block_date"], "%Y-%m-%d"
            ).date()

    def __convert_models(
        self,
        data: dict,
        data_key: str,
        repo_key: str,
        dto_type: type,
        model_type: type,
    ) -> bool:
        vld.is_dict(data, "data")
        vld.is_str(data_key, "data_key")
        vld.is_str(repo_key, "repo_key")

        items = data.get(data_key, [])
        if not items:
            return False
        
        converted_count = 0
        for item in items:
            if self.__repository.get_by_name(item.get("name", "")):
                continue
            
            dto = dto_type().load(item)
            model = model_type.from_dto(dto, self.__repository)
            self.__repository.data[repo_key][model.name] = model
            converted_count += 1
        
        # Логируем конвертацию
        if converted_count > 0:
            self._logger.log_debug(f"Converted {converted_count} {data_key}", {
                "data_key": data_key,
                "repo_key": repo_key,
                "converted_count": converted_count
            })
        
        return True
    
    def __convert_nomenclature_groups(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenclature_groups",
            repo_key=Repository.nomenclature_group_key,
            dto_type=NomenclatureGroupDto,
            model_type=NomenclatureGroupModel
        )
    
    def __convert_measure_units(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="measure_units",
            repo_key=Repository.measure_unit_key,
            dto_type=MeasureUnitDto,
            model_type=MeasureUnitModel
        )
    
    def __convert_nomenlatures(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="nomenlatures",
            repo_key=Repository.nomenclatures_key,
            dto_type=NomenclatureDto,
            model_type=NomenclatureModel
        )

    def __convert_recipes(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="recipes",
            repo_key=Repository.recipes_key,
            dto_type=RecipeDto,
            model_type=RecipeModel
        )
    
    def __convert_transactions(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="transactions",
            repo_key=Repository.transactions_key, 
            dto_type=TransactionDto, 
            model_type=TransactionModel  
        )
    
    def __convert_storages(self, data: dict) -> bool:
        return self.__convert_models(
            data=data,
            data_key="storages",
            repo_key=Repository.storages_key,
            dto_type=StorageDto,
            model_type=StorageModel 
        )

    def convert_ost(self, block_date: date = None) -> bool:
        from src.logics.osd_tbs import OsdTbs
        if block_date is None:
            # Пытаемся загрузить из файла остатков
            if self.load_repository_data():
                return True
            else:
                raise OperationException(
                    "Block date is not specified and no saved OST data found"
                )
        
        # Проверяем, совпадает ли block_date с сохраненным
        if (self.repository.block_date and 
            self.repository.block_date == block_date and
            self.repository.headers and 
            self.repository.turnovers_history):
            self._logger.log_debug("Using cached OST data", {
                "block_date": block_date
            })
            return True
        
        # Вычисляем новые данные
        self._logger.log_info("Calculating OST data", {
            "block_date": block_date
        })
        
        headers, display_data_rows, work_transactions, display_data_dict = OsdTbs.calculate_ost(block_date, self)
        
        self.repository.headers = headers
        self.repository.turnovers_history = display_data_rows
        self.repository.next_transactions = work_transactions
        self.repository.display_data_dict = display_data_dict
        self.repository.block_date = block_date
        
        # Логируем результаты
        self._logger.log_info("OST calculation completed", {
            "block_date": block_date,
            "headers_count": len(headers),
            "turnovers_count": len(display_data_rows),
            "transactions_count": len(work_transactions)
        })
        
        self.save_repository_data()
        return True

    def convert(self, data: dict, block_date: date = None) -> bool:
        vld.is_dict(data, "data")
        
        self._logger.log_debug("Starting data conversion")
        
        # Конвертируем все модели
        conversion_results = {}
        conversion_results["nomenclature_groups"] = self.__convert_nomenclature_groups(data)
        conversion_results["measure_units"] = self.__convert_measure_units(data)
        conversion_results["nomenclatures"] = self.__convert_nomenlatures(data)
        conversion_results["recipes"] = self.__convert_recipes(data)
        conversion_results["storages"] = self.__convert_storages(data) 
        conversion_results["transactions"] = self.__convert_transactions(data)
        
        # Логируем результаты конвертации
        self._logger.log_info("Data conversion completed", {
            "conversion_results": conversion_results,
            "total_items": sum(len(models) for models in self.__repository.data.values())
        })
        
        if block_date:
            self.__repository.block_date = block_date
            self.convert_ost(block_date)
        
        return True
    
    def start(self, file_name: str):
        self.file_name = file_name
        self.load()
        
        # Логируем запуск сервиса
        self._logger.log_info("StartService started", {
            "file": file_name,
            "block_date": self.block_date,
            "settings_file": self.__settings_manager.file_name
        })

    def save_data(self):
        """Сохраняет все данные в файл"""
        try:
            if not self.file_name:
                raise OperationException("Файл данных не указан")
            
            # Сохраняем основной репозиторий
            self.save_repository(self.file_name)
            
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_data",
                "status": "success",
                "file_path": self.file_name
            })
            
            self._logger.log_info("Data saved successfully", {
                "file": self.file_name
            })
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_data",
                "status": "error",
                "error": f"Ошибка сохранения данных: {e}"
            })
            self._logger.log_error("Error saving data", {
                "error": str(e)
            })

    # Методы для работы с элементами репозитория
    def __save_item(self, key: str, model):
        """Сохраняет элемент в репозитории"""
        vld.validate(key, str, "key")
        # Используем unique_code из модели
        self.__repository.data[key][model.unique_code] = model

    def __pop_item(self, key: str, model):
        """Удаляет элемент из репозитория"""
        vld.validate(key, str, "key")
        if model.unique_code in self.__repository.data[key]:
            del self.__repository.data[key][model.unique_code]

    def _add_reference(self, reference_type: str, properties: dict):
        """Добавляет новый элемент справочника"""
        try:
            if reference_type not in self.__reference_mapping:
                raise OperationException(f"Неизвестный тип справочника: {reference_type}")
            
            dto_type, model_type = self.__reference_mapping[reference_type]
            dto = dto_type().load(properties)
            model = model_type.from_dto(dto, self.repository)
            
            # Сохраняем в репозиторий
            repo_key = self._get_repo_key(reference_type)
            self.__save_item(repo_key, model)
            
            # Логируем добавление
            self._logger.log_info(f"Reference added: {reference_type}", {
                "type": reference_type,
                "name": properties.get('name', 'unknown'),
                "unique_code": model.unique_code
            })
            
            observe_service.create_event(event_type.reference_added(), {
                "type": reference_type,
                "name": properties.get('name', 'unknown'),
                "properties": properties
            })
            
            self.save_data()
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "add_reference",
                "status": "error",
                "error": f"Ошибка добавления {reference_type}: {e}"
            })
            self._logger.log_error(f"Error adding reference: {reference_type}", {
                "error": str(e),
                "properties": properties
            })
            raise

    def _change_reference(self, reference_type: str, unique_code: str, properties: dict):
        """Изменяет элемент справочника"""
        try:
            # Находим старую модель
            old_model = self.repository.get_by_unique_code(unique_code)
            if not old_model:
                raise OperationException(f"Объект с кодом {unique_code} не найден")
            
            if reference_type not in self.__reference_mapping:
                raise OperationException(f"Неизвестный тип справочника: {reference_type}")
            
            # Создаем новую модель
            dto_type, model_type = self.__reference_mapping[reference_type]
            updated_properties = {**self._model_to_dict(old_model), **properties}
            dto = dto_type().load(updated_properties)
            new_model = model_type.from_dto(dto, self.repository)
            
            # Рассылаем событие обновления зависимостей
            observe_service.create_event(event_type.update_dependencies(), {
                "old_model": old_model,
                "new_model": new_model
            })
            
            # Заменяем модель в репозитории
            repo_key = self._get_repo_key(reference_type)
            self.__pop_item(repo_key, old_model)
            self.__save_item(repo_key, new_model)
            
            # Логируем изменение
            self._logger.log_info(f"Reference updated: {reference_type}", {
                "type": reference_type,
                "unique_code": unique_code,
                "old_name": old_model.name,
                "new_name": new_model.name
            })
            
            observe_service.create_event(event_type.reference_updated(), {
                "type": reference_type,
                "unique_code": unique_code,
                "properties": properties
            })
            
            self.save_data()
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "change_reference",
                "status": "error",
                "error": f"Ошибка изменения {reference_type}: {e}"
            })
            self._logger.log_error(f"Error changing reference: {reference_type}", {
                "error": str(e),
                "unique_code": unique_code,
                "properties": properties
            })
            raise

    def _remove_reference(self, reference_type: str, unique_code: str):
        """Удаляет элемент справочника"""
        try:
            # Находим модель
            model = self.repository.get_by_unique_code(unique_code)
            if not model:
                raise OperationException(f"Объект с кодом {unique_code} не найден")
            
            # Проверяем зависимости
            observe_service.create_event(event_type.check_dependencies(), {"model": model})
            
            # Удаляем если нет зависимостей
            repo_key = self._get_repo_key(reference_type)
            self.__pop_item(repo_key, model)
            
            # Логируем удаление
            self._logger.log_warning(f"Reference deleted: {reference_type}", {
                "type": reference_type,
                "unique_code": unique_code,
                "name": model.name
            })
            
            observe_service.create_event(event_type.reference_deleted(), {
                "type": reference_type,
                "unique_code": unique_code
            })
            
            self.save_data()
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "remove_reference",
                "status": "error",
                "error": f"Ошибка удаления {reference_type}: {e}"
            })
            self._logger.log_error(f"Error removing reference: {reference_type}", {
                "error": str(e),
                "unique_code": unique_code
            })
            raise

    def _get_repo_key(self, reference_type: str) -> str:
        """Получает ключ репозитория для типа справочника"""
        keys = {
            "nomenclatures": Repository.nomenclatures_key,
            "measure_units": Repository.measure_unit_key,
            "nomenclature_groups": Repository.nomenclature_group_key,
            "storages": Repository.storages_key,
            "transactions": Repository.transactions_key,
            "recipes": Repository.recipes_key
        }
        return keys.get(reference_type, reference_type)

    def _model_to_dict(self, model) -> Dict[str, Any]:
        """Конвертирует модель в словарь"""
        try:
            converter = FactoryConverters()
            return converter.convert(model)
        except:
            # Fallback конвертация
            result = {}
            if hasattr(model, '__dict__'):
                for key, value in model.__dict__.items():
                    if not key.startswith('_'):
                        result[key] = value
            return result

    def __convert_to_required_format(self) -> Dict[str, Any]:
        """Конвертирует данные в требуемый формат с массивами объектов"""
        result = {}
        
        # Конвертируем каждую группу моделей в массив
        result["measure_model"] = [self._model_to_dict(model) for model in self.measure_units.values()]
        result["nomenclature_group_model"] = [self._model_to_dict(model) for model in self.nomenclature_groups.values()]
        result["nomenclature_model"] = [self._model_to_dict(model) for model in self.nomenclatures.values()]
        result["recipe_model"] = [self._model_to_dict(model) for model in self.recipes.values()]
        result["storage_model"] = [self._model_to_dict(model) for model in self.storages.values()]
        result["transaction_model"] = [self._model_to_dict(model) for model in self.transactions.values()]
        result["rest_model"] = []  # Пустой массив, как в примере
        
        # Добавляем дополнительные поля
        result["block_date"] = self.block_date.strftime("%Y-%m-%d")
        result["first_start"] = getattr(self.__settings_manager.settings, 'first_start', False)
        
        return result

    def save_repository(self, file_path: str):
        """Сохраняет основной репозиторий в файл в требуемом формате"""
        try:
            abs_path = os.path.abspath(file_path)
            
            # Создаем событие о начале сохранения
            observe_service.create_event(event_type.convert_to_json(), {
                "file": abs_path,
                "operation": "start_saving"
            })
            
            # Логируем начало сохранения
            self._logger.log_info("Saving repository", {
                "file": abs_path,
                "model_counts": {
                    "measure_units": len(self.measure_units),
                    "nomenclature_groups": len(self.nomenclature_groups),
                    "nomenclatures": len(self.nomenclatures),
                    "recipes": len(self.recipes),
                    "storages": len(self.storages),
                    "transactions": len(self.transactions)
                }
            })
            
            # Конвертируем данные в требуемый формат
            result = self.__convert_to_required_format()
            
            # Создаем директорию если не существует
            file_dir = os.path.dirname(abs_path)
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)
            
            with open(abs_path, 'w', encoding='utf-8') as file:
                json.dump(object_to_dto(result), file, ensure_ascii=False, indent=2)
            
            # Логируем успешное сохранение
            self._logger.log_info("Repository saved successfully", {
                "file": abs_path,
                "total_items": sum(len(arr) for arr in result.values() if isinstance(arr, list))
            })
            
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_repository",
                "status": "success",
                "file_path": abs_path
            })
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_repository",
                "status": "error",
                "error": f"Ошибка сохранения основного репозитория: {e}"
            })
            self._logger.log_error("Error saving repository", {
                "file": file_path,
                "error": str(e)
            })
            raise OperationException(f"Не удалось сохранить репозиторий: {e}")

    def __save_settings_file(self, file_path: str):
        """Сохраняет настройки в файл appsettings.json в исходном формате"""
        try:
            # Загружаем текущие настройки
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                current_settings = json.load(file)
            
            # Обновляем только block_date
            current_settings["block_date"] = self.block_date.strftime("%Y-%m-%d")
            
            # Сохраняем обратно
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(current_settings, file, ensure_ascii=False, indent=2)
            
            self._logger.log_info("Settings saved", {
                "file": file_path,
                "block_date": self.block_date
            })
            
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_settings",
                "status": "success",
                "file_path": file_path
            })
            
        except Exception as e:
            observe_service.create_event(event_type.reference_operation_completed(), {
                "operation": "save_settings",
                "status": "error",
                "error": f"Ошибка сохранения настроек: {e}"
            })
            self._logger.log_error("Error saving settings", {
                "file": file_path,
                "error": str(e)
            })
            raise OperationException(f"Не удалось сохранить настройки: {e}")

    """
    Обработка событий
    """
    def handle(self, event: str, params: dict):
        super().handle(event, params)

        if event == event_type.add_reference():
            reference_type = params["model"]
            properties = params["properties"]
            self._add_reference(reference_type, properties)
            
        elif event == event_type.change_reference():
            reference_type = params["model"]["type"]
            unique_code = params["model"]["unique_code"]
            properties = params["properties"]
            self._change_reference(reference_type, unique_code, properties)
            
        elif event == event_type.remove_reference():
            reference_type = params["model"]["type"]
            unique_code = params["model"]["unique_code"]
            self._remove_reference(reference_type, unique_code)
            
        elif event == event_type.change_block_period():
            new_block_date = params["new_block_date"]
            vld.validate(new_block_date, date, "new_block_date")
            self.block_date = new_block_date
            self.convert_ost()
            self.__save_settings_file("appsettings.json")