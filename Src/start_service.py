from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from typing import Callable, Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Рецепт по умолчанию
    __default_receipt: receipt_model

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __default_receipt_items = {}

    # Наименование файла (полный путь)
    __full_file_name: str = ""

    def __init__(self):
        self.__repo.initalize()

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

        # Текущий файл

    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            file_name = self.__full_file_name.encode('utf-8').decode('utf-8')
            with open(file_name, 'r', encoding='utf-8') as file_instance:
                print(self.__full_file_name)
                settings = json.load(file_instance)

                if "default_receipt" in settings.keys():
                    data = settings["default_receipt"]
                    return self.convert(data)

            return False
        except Exception as e:
            logging.error(f"Ошибка при загрузке файла: {e}")
            return False

    # Фабрика для создания объектов модели
    def _create_model_instance(self, model_type: str, data: Dict[str, Any]) -> Optional[Any]:
        """Создает экземпляр объекта модели на основе типа и данных."""
        name = data.get('name', "")
        id = data.get('id', "")
        if id.strip() == "":
            return None

        try:
            if model_type == "range_model":
                base_id = data.get('base_id', "")
                value = data.get('value', 1)
                base = self.__default_receipt_items.get(base_id)
                item = range_model.create(name, value, base)
            elif model_type == "group_model":
                item = group_model.create(name)
            elif model_type == "nomenclature_model":
                range_id = data.get('range_id', "")
                category_id = data.get('category_id', "")
                range_item = self.__default_receipt_items.get(range_id)
                category_item = self.__default_receipt_items.get(category_id)
                item = nomenclature_model.create(name, category_item, range_item)
            else:
                raise ValueError(f"Неподдерживаемый тип модели: {model_type}")

            item.unique_code = id
            return item
        except Exception as e:
            logging.error(f"Ошибка при создании экземпляра {model_type}: {e}")
            return None

    def _convert_items(self, data: Dict[str, Any], key: str, model_type: str) -> bool:
        """
        Универсальный метод для конвертации элементов определенного типа.

        Args:
            data: Словарь с данными.
            key: Ключ, под которым находится список элементов в data (например, 'ranges', 'categories').
            model_type: Тип модели для создания экземпляров (например, 'range_model').

        Returns:
            True, если конвертация прошла успешно, False в случае ошибки.
        """
        validator.validate(data, dict)
        items = data.get(key, [])
        for item_data in items:
            try:
                item = self._create_model_instance(model_type, item_data)
                if item:
                    self.__default_receipt_items.setdefault(item.unique_code, item)
                    self.__repo.data.setdefault(self.get_key(model_type), []).append(item)
            except Exception as e:
                logging.error(f"Ошибка при конвертации {model_type}: {e}")
                return False
        return True

    # Загрузить единицы измерений
    def __convert_ranges(self, data: dict) -> bool:
        return self._convert_items(data, 'ranges', 'range_model')

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        return self._convert_items(data, 'categories', 'group_model')

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        return self._convert_items(data, 'nomenclatures', 'nomenclature_model')

    # Обработать полученный словарь
    def convert(self, data: dict) -> bool:
        """
        Обрабатывает полученный словарь с данными рецепта, преобразует данные в объекты моделей и сохраняет их в репозитории.
        Выполняет проверки данных и обрабатывает исключения для обеспечения стабильной работы.
        """
        validator.validate(data, dict)

        try:
            # 1 Созданим рецепт
            cooking_time = data.get('cooking_time', "")
            portions = data.get('portions', 0)
            if not isinstance(portions, int):
                logging.error(f"Некорректный тип данных для 'portions': {portions}. Ожидается int.")
                return False  # Возвращаем False при ошибке валидации

            name = data.get('name', "НЕ ИЗВЕСТНО")
            self.__default_receipt = receipt_model.create(name, cooking_time, portions)

            # Загрузим шаги приготовления
            steps = data.get('steps', [])
            if not isinstance(steps, list):
                logging.error(f"Некорректный тип данных для 'steps': {steps}. Ожидается list.")
                return False

            for step in steps:
                if not isinstance(step, str):
                    logging.warning(f"Некорректный тип данных для шага приготовления: {step}. Ожидается str.")
                    continue  # Пропускаем некорректный шаг

                if step.strip() != "":
                    self.__default_receipt.steps.append(step)

            if not self.__convert_ranges(data):
                logging.error("Ошибка при конвертации ranges.")
                return False

            if not self.__convert_groups(data):
                logging.error("Ошибка при конвертации groups.")
                return False

            if not self.__convert_nomenclatures(data):
                logging.error("Ошибка при конвертации nomenclatures.")
                return False

            # Собираем рецепт
            compositions = data.get('composition', [])
            if not isinstance(compositions, list):
                logging.error(f"Некорректный тип данных для 'composition': {compositions}. Ожидается list.")
                return False

            for composition in compositions:
                nomenclature_id = composition.get('nomenclature_id', "")
                range_id = composition.get('range_id', "")
                value = composition.get('value', "")

                if not (nomenclature_id and range_id and value):
                    logging.warning(
                        f"Пропущена запись в 'composition' из-за отсутствия nomenclature_id, range_id или value: {composition}")
                    continue

                nomenclature = self.__default_receipt_items.get(nomenclature_id)
                range_item = self.__default_receipt_items.get(range_id)

                if not nomenclature or not range_item:
                    logging.warning(
                        f"Пропущена запись в 'composition' из-за отсутствия nomenclature или range_item. nomenclature_id: {nomenclature_id}, range_id: {range_id}")
                    continue

                item = receipt_item_model.create(nomenclature, range_item, value)
                self.__default_receipt.composition.append(item)

            # Сохраняем рецепт
            self.__repo.data[reposity.receipt_key()].append(self.__default_receipt)
            return True

        except Exception as e:
            logging.exception(f"Ошибка при конвертации данных: {e}")
            return False

    """
    Стартовый набор данных
    """

    @property
    def data(self):
        return self.__repo.data

    """
    Основной метод для генерации эталонных данных
    """

    def start(self):
        self.file_name = "settings.json"
        result = self.load()
        if result == False:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")

    def get_key(self, model_type: str) -> str:
        if model_type == "range_model":
            return reposity.range_key()
        elif model_type == "group_model":
            return reposity.group_key()
        elif model_type == "nomenclature_model":
            return reposity.nomenclature_key()
        elif model_type == "receipt_model":
            return reposity.receipt_key()
        else:
            raise ValueError(f"Неподдерживаемый тип модели: {model_type}")

