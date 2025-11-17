from src.core.abstract_dto import AbstractDto
from src.core.abstract_model import AbstractModel
from typing import Self
class FiltredDto(AbstractDto):
    __field_name:str=""
    __value:AbstractModel=None
    __operator:str=""
    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
        
    @property
    def field_name(self)->str:
        return self.__field_name
    @field_name.setter
    def field_name(self,value:str)->str:
        self.__field_name=value
    @property
    def value(self)->AbstractModel:
        return self.__value
    @value.setter
    def value(self,value:AbstractModel)->AbstractModel:
        self.__value=value
    @property
    def operator(self)->str:
        return self.__operator
    @operator.setter
    def operator(self,operator:str)->str:
        self.__operator=operator
    def load(self, data) -> Self:
        super().load(data)
        self.field_name = data["field_name"]
        self.value = data["value"]
        return self