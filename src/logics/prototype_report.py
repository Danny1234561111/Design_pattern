from src.core.prototype import Prototype
from src.models.nomenclature_model import NomenclatureModel
from src.core.validator import Validator
from src.dtos.filter_dto import FiltredDto
#Реализация прототипа
class PrototypeReport(Prototype):
    @staticmethod
    def filter(source: Prototype, filter: FiltredDto):
        Validator.validate(source, Prototype,"source")
        Validator.validate(filter, FiltredDto,"filtred")
        result = Prototype.filter(source.data, filter)
        return source.clone(result)
        

