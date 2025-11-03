from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.abstract_converter import AbstractConverter
from src.utils import get_properties


"""Конвертер, обрабатывающий объекты, являющиеся AbstractModel"""
class ReferenceConverter(AbstractConverter):
    
    def __init__(self):
        super().__init__()
    
    """Переопределённый метод convert
    
    Проходится по полям AbstractModel и формирует словарь формата
    'поле: конвертированное значение поля'
    """
    def convert(self, object_: AbstractModel) -> dict:
        from src.logics.factory_converters import FactoryConverters

        vld.validate(object_, AbstractModel, "object")

        factory = FactoryConverters()
        result = dict()
        props = get_properties(object_)
        for prop in props:
            value = getattr(object_, prop)

            if isinstance(value, AbstractModel):
                result[prop] = self.convert(value)
            else:
                result[prop] = factory.create(value).convert(value)

        return result
