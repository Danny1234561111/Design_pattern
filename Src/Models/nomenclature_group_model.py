from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model
class nomenclature_group_model(abstact_model):
    __name: str = ""
    def __init__(self,name:str=""):
        self.__name=name
    @property
    def name(self,name="") -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value.strip()