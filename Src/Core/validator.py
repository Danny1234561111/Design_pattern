import os
from typing import Any, List
class argument_exception(Exception):
    pass

class operation_exception(Exception):
    pass
def obj_to_dict(object_: Any) -> dict:
    
    # Если объект - словарь
    if type(object_) is dict:
        d = dict()
        for k, v in object_.items():
            d[k] = obj_to_dict(v)
        return d
    # Если итерируемый объект
    elif type(object_) in [list, tuple]:
        l = list()
        for item in object_:
            l += [obj_to_dict(item)]
        return l
    # Если объект - AbstractModel с полем 'name'
    elif isinstance(object_, AbstractModel):
        return {prop: obj_to_dict(getattr(object_, prop))
                for prop in get_properties(object_)}
    # Если примитивный тип
    elif type(object_) in [bool, int, float, str] or object_ is None:
        return object_
    # Всё остальное
    else:
        return str(object_)
class validator:
    @staticmethod
    def is_structure(value, arg_name: str) -> None:
        if not isinstance(value, (dict, list, tuple)):
            raise argument_exception(f"Аргумент '{arg_name}' должен быть словарем, списком или кортежем.")

    @staticmethod
    def validate(value, type_, len_=None):
        if value is None:
            raise argument_exception("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

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
        if not isinstance(file_path, str):
            raise argument_exception("Путь к файлу должен быть строкой")
        
        return os.path.isfile(file_path)

    @staticmethod
    def is_dict(value, arg_name: str) -> None:
        if not isinstance(value, dict):
            raise argument_exception(f"Аргумент '{arg_name}' должен быть словарем (dict)")
    
    
