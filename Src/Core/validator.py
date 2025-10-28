import os
from typing import Any

class argument_exception(Exception):
    pass

class operation_exception(Exception):
    pass

class validator:

    @staticmethod
    def validate(value, type_, len_=None):
        """
        Валидация аргумента по типу и длине.
        
        Args:
            value (any): Аргумент.
            type_ (object): Ожидаемый тип.
            len_ (int): Максимальная длина.
        
        Raises:
            argument_exception: Некорректный тип или длина.
        
        Returns:
            True или исключение.
        """
        if value is None:
            raise argument_exception("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип! Ожидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента на пустоту (только если это строка)
        if type_ is str and len(str(value).strip()) == 0:
            raise argument_exception("Пустой аргумент")

        # Проверка длины (только если это строка и len_ указана)
        if type_ is str and len_ is not None:
            if not isinstance(len_, int):
                raise argument_exception("Длина должна быть числом")
            if len(str(value).strip()) > len_:
                raise argument_exception("Некорректная длина аргумента")

        return True

    @staticmethod
    def is_file_exists(file_path: str) -> bool:
        """
        Проверка существования файла по заданному пути.

        Args:
            file_path (str): Путь к файлу.

        Returns:
            bool: True, если файл существует, иначе False.
        """
        if not isinstance(file_path, str):
            raise argument_exception("Путь к файлу должен быть строкой")
        
        return os.path.isfile(file_path)

    @staticmethod
    def is_dict(value, arg_name: str) -> None:
        if not isinstance(value, dict):
            raise argument_exception(f"Аргумент '{arg_name}' должен быть словарем (dict)")

    @staticmethod
    def is_structure(value: Any, arg_name: str) -> None:
        if not isinstance(value, (list, tuple, dict)):
            raise argument_exception(f"Аргумент '{arg_name}' должен быть списком, кортежем или словарем.")