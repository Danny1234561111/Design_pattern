import os

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
            ArgumentException: Некорректный тип.
            ArgumentException: Пустой аргумент.
            ArgumentException: Некорректная длина аргумента.
        
        Returns:
            True или исключение.
        """
        if value is None:
            raise ArgumentException("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise ArgumentException(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента на пустоту (только если это строка)
        if type_ is str and len(str(value).strip()) == 0:
            raise ArgumentException("Пустой аргумент")

        # Проверка длины (только если это строка и len_ указана)
        if type_ is str and len_ is not None:
            if not isinstance(len_, int):
                raise ArgumentException("Длина должна быть числом")
            if len(str(value).strip()) > len_:
                raise ArgumentException("Некорректная длина аргумента")

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
            raise ArgumentException("Путь к файлу должен быть строкой")
        
        return os.path.isfile(file_path)

# Пример использования
class StartService:
    def __init__(self, file_name: str):
        self.file_name = file_name

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = validator.is_file_exists(value)
