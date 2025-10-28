from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.common import common
from typing import Dict, Any
class reference_convertor(abstract_convertor):

    # Формируется словарь в виде "поле класса": converter.convert(значение поля), где тип converter умеет обрабатывать тип поля.
    def convert(self, obj: Any) -> dict: # Change type hint to Any
        from Src.Convert.convert_factory import FactoryConvertors
        # validator.validate(obj, abstact_reference) # Remove validation
        factory = FactoryConvertors()
        result = {}
        properties = common.get_fields(obj)
        for property in properties:
            value = getattr(obj, property)
            # if isinstance(value, abstact_reference): # Remove this check
            #     result[property] = self.convert(value)
            # else:
            result[property] = factory.convert(value)
        return result