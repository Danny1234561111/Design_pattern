from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model

class storage_model(abstact_model):
    __name: str = ""
    def __init__(self,name:str=""):
        self.__name=name
    # Наименование
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        validator.validate(value, str)
        self.__name = value.strip()
