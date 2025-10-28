from typing import Any, Union, Dict, List, Type
from datetime import datetime
from Src.Core.exceptions import ParamException
from Src.Core.abstract_model import abstact_model
from Src.Core.abstract_convertor import abstract_convertor
from Src.Convert.basic_convertor import basic_convertor
from Src.Convert.datetime_convertor import datetime_convertor
from Src.Convert.reference_convertor import reference_convertor
from typing import Any, Union, Dict, List, Type
from datetime import datetime
from Src.Convert.structure_convertor import StructureConvertor
from Src.Core.validator import validator

class FactoryConvertors:
    _converters: Dict[Type, Type[abstract_convertor]] = {
        bool: basic_convertor,
        int: basic_convertor,
        float: basic_convertor,
        str: basic_convertor,
        type(None): basic_convertor,  # Обработка None
        datetime: datetime_convertor,
        abstact_model: reference_convertor  # Важно: не type(AbstractModel), а сам класс AbstractModel
    }

    def create(self, object_: Any) -> abstract_convertor:
        if isinstance(object_, (list, dict, tuple)):
            return StructureConvertor()  # Возвращаем конвертер для структур

        for type_, converter_class in self._converters.items():
            if isinstance(object_, type_) or type_ is type(object_):
                return converter_class()

        raise ParamException(
            f"Impossible to create converter from object "
            f"with type '{type(object_).__name__}'"
        )

    def convert(self, object_: Any) -> Union[Dict, List]:
        return self.create(object_).convert(object_)
