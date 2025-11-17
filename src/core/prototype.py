from src.core.validator import Validator
from src.dtos.filter_dto import FiltredDto
from typing import List,Any
from src.core.filter_operators import filter_operators
from datetime import datetime, date
from typing import List, Any, Callable, Dict, Union

class Prototype:
    __data=[]
    
    def __init__(self,data:list):
        Validator.validate(data,list,"data")
        self.data=data
    def data(self):
        return self.__data
    def clone(self,data:list=None) -> "Prototype":
        if data is None:
            inner_data=self.__data
        else:
            inner_data = data
        instance = Prototype(inner_data)
        return instance
    def filter(data: list, filter_dto: FiltredDto) -> List[Any]:
        """
        Фильтрует данные экземпляра на основе объекта FiltredDto.
        Выполняет сравнения с учетом типов для datetime/date и других.
        """
        operators: Dict[str, Callable[[Any, Any], bool]] = {
            filter_operators.equals(): lambda a, b: a == b,
            # Для 'like' преобразуем оба значения в строки и в нижний регистр для регистронезависимого поиска.
            # Обрабатываем None, чтобы избежать ошибок AttributeError или TypeError.
            filter_operators.like(): lambda a, b: (str(b).lower() in str(a).lower()) if a is not None and b is not None else False,
            filter_operators.less(): lambda a, b: a < b,
            filter_operators.greater(): lambda a, b: a > b,
            filter_operators.not_less(): lambda a, b: a >= b,
            filter_operators.not_greater(): lambda a, b: a <= b
        }
        # Валидируем объект фильтра
        Validator.validate(filter_dto, FiltredDto, "filter_dto")
        if not data: # Если данных нет, возвращаем пустой список
            return []
        result: List[Any] = []
        
        # Получаем функцию оператора из _OPERATORS.
        operator_func = operators.get(filter_dto.operator)
        if not operator_func:
            raise ValueError(f"Неподдерживаемый оператор фильтра: '{filter_dto.operator}'")
        result=[]
        for item in data:
            # Получаем значение поля для текущего элемента
                value = getattr(item, filter_dto.field_name, None)
                # Выполняем сравнение
                if operator_func(filter_dto.value,value.name):
                    result.append(item)
        return result