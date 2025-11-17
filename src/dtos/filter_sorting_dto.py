from src.dtos.filter_dto import FiltredDto
from src.core.validator import Validator

class filter_sorting_dto:
    """
    DTO для передачи параметров фильтрации и сортировки
    Используется в методах фильтрации prototype
    """

    __filters = []

    @property
    def filters(self) -> list:
        return self.__filters

    def __init__(self, filters):
        self.__filters = filters