from Src.Core.entity_model import entity_model
from Src.Core.abstract_dto import abstact_dto

"""
Модель группы номенклатуры
"""
class group_model(entity_model):
    __unique_code: str = ""


    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        self.__unique_code = value

    """
    Заводской метод из Dto
    """
    @staticmethod
    def from_dto(dto: abstact_dto):
        item = group_model(dto.name, dto.id) # Передаем аргументы в конструктор
        #item.name = dto.name  # Больше не нужно, так как устанавливается в конструкторе
        #item.unique_code = dto.id # Больше не нужно, так как устанавливается в конструкторе
        return item

    def to_dto(self) -> abstact_dto:
        dto = abstact_dto()
        dto.name = self.name
        dto.id = self.unique_code
        return dto