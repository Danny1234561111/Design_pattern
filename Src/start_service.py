import os
import json
from Src.reposity import reposity
from Src.Models.company_model import company_model
from Src.Core.validator import validator, argument_exception, operation_exception
from Src.Models.receipt_model import ReceiptModel
class start_service:
    __instance = None
    _reposity: reposity = reposity()
    __file_name: str = ""

    def __init__(self):
        if self._reposity is None:
            self._reposity = reposity()
        self._reposity.initialize()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Файл "{value}" не найден.')

    def load(self) -> bool:
        if not self.__file_name:
            raise operation_exception("Файл конфигурации не задан.")
        
        try:
            with open(self.__file_name, 'r', encoding="utf-8") as file:
                content = file.read().strip()

                if not content:
                    raise operation_exception("Файл конфигурации пуст.")

                objects = json.loads(content)

                # Проверка наличия ключей "company" и "default_receipt"
                if "company" not in objects or "default_receipt" not in objects:
                    raise operation_exception("В файле отсутствует секция 'company' или 'default_receipt'.")

                company_data = objects["company"]
                if not self.__convert_company(company_data):
                    raise operation_exception("Ошибка при загрузке данных компании.")

                receipt_data = objects["default_receipt"]

                # Используем метод convert у ReceiptModel
                receipt_instance = ReceiptModel()
                receipt_instance.convert(receipt_data)
                self._reposity.data['receipt_model'] = receipt_instance  # Хранение модели

                return True

        except FileNotFoundError:
            raise operation_exception(f"Файл '{self.__file_name}' не найден.")
        except json.JSONDecodeError as e:
            raise operation_exception(f"Ошибка при чтении файла '{self.__file_name}': неверный формат JSON: {e}")
        except Exception as e:
            raise operation_exception(f"Ошибка при загрузке файла: {str(e)}")

    def start(self, settings_file: str):
        """Метод для инициализации сервиса с использованием файла настроек."""
        self.file_name = settings_file  # Устанавливаем файл настроек
        self.load()  # Загружаем настройки

    def __convert_company(self, data: dict) -> bool:
        validator.validate(data, dict)
        if not data:
            return False

        company_instance = company_model()
        if 'name' in data:
            company_instance.name = data['name']
        if 'inn' in data:
            company_instance.inn = data['inn']
        self._reposity.data['company'] = company_instance
        return True

    def get_receipts(self) -> list:
        """Метод для получения всех рецептов."""
        return self._reposity.data.get('receipt_model', [])

    def get_receipt(self, receipt_id: int) -> dict:
        """Метод для получения конкретного рецепта по его ID."""
        receipts = self.get_receipts()
        for receipt in receipts:
            if receipt.id == receipt_id:  # Предположим, что в ReceiptModel есть свойство id
                return receipt
        raise operation_exception(f"Рецепт с ID {receipt_id} не найден.")