from typing import Any, List
from src.core.exceptions import ParamException
from src.core.abstract_model import AbstractModel


"""Возвращает список полей и методов переданного объекта"""
def get_fields(object_: Any) -> List[str]:
    if object_ is None:
        raise ParamException(f"Object can't be none")
    
    return [f for f in dir(object_) if not f.startswith("_")]


"""Возвращает список не-callable полей объекта"""
def get_properties(object_: Any) -> List[str]:
    if object_ is None:
        raise ParamException(f"Object can't be none")
    
    fields = get_fields(object_)
    return [f for f in fields if not callable(getattr(object_, f))]


"""Представляет переданный объект в строковом представлении"""
def obj_to_str(object_: Any) -> str:
    # Если объект - словарь
    if type(object_) is dict:
        dict_items = [f"{k}: {obj_to_str(v)}" for k, v in object_.items()]
        return ("{" +
                ", ".join(dict_items) +
                "}")
    # Если итерируемый объект
    elif type(object_) in [list, tuple]:
        return ("[" +
                ", ".join([obj_to_str(item) for item in object_]) + 
                "]")
    # Если объект - AbstractModel с полем 'name'
    elif isinstance(object_, AbstractModel):
        return object_.name
    # Любой другой тип (примитивный, или другой класс)
    else:
        return str(object_)


"""Функция, рекурсивно приводящая объект и его поля к словарю"""
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
