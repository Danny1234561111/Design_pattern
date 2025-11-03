import pathlib
from typing import Optional, Any, Union, Type, List, Tuple, Dict
from src.core.exceptions import (
    InvalidValueException, WrongTypeException, ParamException
)


"""Вспомогательный класс для валидации полей и объектов"""
class Validator:

    """Общий метод валидации значений

    Args:
        value (Any): валидируемое значение.
        types (Union[Type, List[Type]]): тип валидируемого значения
            или список допустимых типов значения.
        field_name (str): строковое название поля.
        could_be_none (bool, optional): может ли поле быть None.
            По-умолчанию False.
        len_ (Optional[int], optional): ожидаемая длина строкового
            представления значения. По-умолчанию False.
        strictly_len (bool, optional): строго ли длина значения
            дожна быть = параметру len_, или может быть <=.
            По умолчанию False.
    
    Returns:
        bool: True если поле прошло валидацию по типу и значению,
            иначе False.
    
    Raises:
        ParamException: неверно переданный параметр types
        NotValidValueException: невалидное значение.
        WrongTypeException: несоответствие типа поля и ожидаемого типа.
    """
    @staticmethod
    def validate(
        value: Any,
        types: Union[Type, Tuple[Type], List[Type]],
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:

        if could_be_none and value is None:
            return True
        elif (not could_be_none and value is None or
              not len(str(value).strip())):
            raise InvalidValueException(
                f"'{field_name}' is none or empty"
            )
        
        if isinstance(types, (tuple, list)):
            # Если types - это массив типов, то value должен являться
            # одним из типов в types, иначе  WrongTypeException
            flag = False
            for type_ in types:
                if isinstance(value, type_):
                    flag = True
                    break
            if not flag:
                types = [t.__name__ for t in types]
                raise WrongTypeException(
                    f"'{field_name}' must be {', or '.join(types)}, "
                    f"not '{type(value).__name__}'"
                )
        elif isinstance(types, type):
            if not isinstance(value, types):
                raise WrongTypeException(
                    f"'{field_name}' is {type(value).__name__}, not {types.__name__}"
                )
        else:
            raise ParamException(
                "Param 'types' must be either type or list/tuple of types, "
                f"not {type(types).__name__}"
            )
        
        if len_:
            real_len = len(str(value).strip())
            if not strictly_len and real_len > len_:
                raise InvalidValueException(
                    f"Length of '{field_name}' must be less than {len_}, "
                    f"now it's {real_len}"
                )
            elif strictly_len and real_len != len_:
                raise InvalidValueException(
                    f"Length of '{field_name}' must be equal {len_}, "
                    f"now it's {real_len}"
                )
        
        return True

    """Метод проверки на строку"""
    @staticmethod
    def is_str(
        value: str,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, str, field_name,
                                  could_be_none,len_, strictly_len)
    
    """Метод проверки на целочисленное значение"""
    @staticmethod
    def is_int(
        value: int,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, int, field_name,
                                  could_be_none, len_, strictly_len)
    
    """Метод проверки на положительное целое число"""
    @staticmethod
    def is_positive_int(
        value: int,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        result = Validator.is_int(value, field_name,
                                  could_be_none, len_, strictly_len)
        return result if could_be_none else value > 0
    
    """Метод проверки на словарь"""
    @staticmethod
    def is_dict(
        value: dict,
        field_name: str,
        could_be_none: bool = False
    ) -> bool:
        return Validator.validate(value, dict, field_name, could_be_none)

    """Метод проверки на число с плавающей точкой"""
    @staticmethod
    def is_float(
        value: float,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, float, field_name,
                                  could_be_none, len_, strictly_len)
    
    """Метод проверки на число (целое или с плавающей точкой)"""
    @staticmethod
    def is_number(
        value: Union[int, float],
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, (int, float), field_name,
                                  could_be_none, len_, strictly_len)
    
    """Метод проверки на список"""
    @staticmethod
    def is_list(
        value: list,
        field_name: str,
        could_be_none: bool = False,
    ) -> bool:
        return Validator.validate(value, list, field_name, could_be_none)
    
    """
    Метод проверки на список и того, что все его элементы переданного типа
    """
    def is_list_of(
        list_: list,
        types: Union[Type, List[Type], Tuple[Type]],
        list_name: str,
        could_item_be_none: bool = False
    ) -> bool:
        Validator.is_list(list_, list_name)
        for item in list_:
            Validator.validate(item, types, f"item of {list_name}",
                               could_item_be_none)
        return True
    
    """Метод проверки на список и того, что все его элементы одного типа"""
    def is_list_of_same(
        list_: Union[List, Tuple],
        list_name: str,
        could_be_empty: bool = False,
        could_item_be_none: bool = False
    ) -> bool:
        Validator.validate(list_, (list, tuple), list_name)
        if not len(list_):
            if could_be_empty:
                return True
            else:
                raise ParamException(f"List '{list_name}' can't be empty")
        type_ = type(list_[0])
        for i, item in enumerate(list_):
            try:
                Validator.validate(item, type_, f"item of {list_name}",
                                could_item_be_none)
            except WrongTypeException:
                raise WrongTypeException(
                    f"#{i+1} item must be '{type_.__name__}' like "
                    f"first item in list, not '{type(item).__name__}'"
                )
        return True
    
    """Метод проверки на кортеж"""
    @staticmethod
    def is_tuple(
        value: tuple,
        field_name: str,
        could_be_none: bool = False,
    ) -> bool:
        return Validator.validate(value, tuple, field_name, could_be_none)
    
    """Метод проверки на структуру данных (список, словарь или кортеж)"""
    @staticmethod
    def is_structure(
        value: Union[List, Dict, Tuple],
        field_name: str,
        could_be_none: bool = False,
    ) -> bool:
        return Validator.validate(value, (list, dict, tuple), field_name,
                                  could_be_none)

    """Метод проверки на существование файла
    
    Args:
        file_name (str): строка, валидируемая как путь к файлу

    Returns:
        str: абсолютный путь до файла
    
    Raises:
        WrongTypeException: переданное значение не является строкой
        InvalidValueException: пустая строка
        FileNotFoundError: файла по указанному пути не найдено
    """
    @staticmethod
    def is_file_exists(
        file_name: str
    ) -> str:
        if not isinstance(file_name, str):
            raise WrongTypeException(
                f"File name '{file_name}' must be string"
            )
        file_name = file_name.strip()
        if not file_name:
            raise InvalidValueException(
                f"File name '{file_name}' can't be empty"
            )
        if not pathlib.Path(file_name).exists():
            raise FileNotFoundError(f"No such file: {file_name}")
        
        return str(pathlib.Path(file_name).absolute())
    
    """Метод проверки на то, что класс является суперклассом для объекта
    
    Args:
        superclass (type): потенциальный суперкласс
        value (Any): объект, тип которого проверяется то, что он подкласс
            для superclass.
        value_name (str): строковое обозначение value
        could_be_none (bool): может ли value быть None. По умолчанию False.
    
    Returns:
        bool: True, если переданный тип - суперкласс для value,
            иначе False.
    
    Raises:
        WrongTypeException: тип value не является подклассом subclass
    """
    @staticmethod
    def is_superclass(
        superclass: type,
        value: Any,
        value_name: str,
        could_be_none: bool = False
    ) -> bool:
        if could_be_none and value is None:
            return True
        if isinstance(value, superclass):
            return True
        else:
            raise WrongTypeException(
                f"Type of '{value_name}' is {type(value).__name__}, "
                f"which is not subclass of {superclass.__name__}"
            )
