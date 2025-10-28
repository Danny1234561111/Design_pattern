from typing import Any, Dict, Union, Type,List
from datetime import datetime
from Src.Core.exceptions import ParamException
from Src.Core.abstract_model import abstact_model
from Src.Core.abstract_convertor import abstract_convertor
from Src.Convert.basic_convertor import basic_convertor
from Src.Convert.datetime_convertor import datetime_convertor
from Src.Convert.structure_convertor import StructureConvertor
# Импортируем reference_convertor здесь
from Src.Convert.reference_convertor import reference_convertor

class FactoryConvertors:
    _converters: Dict[Type, Type[abstract_convertor]] = {
        bool: basic_convertor,
        int: basic_convertor,
        float: basic_convertor,
        str: basic_convertor,
        type(None): basic_convertor,  # Обработка None
        datetime: datetime_convertor,
        abstact_model: reference_convertor  # Теперь ссылка на reference_convertor
    }

    def create(self, object_: Any) -> abstract_convertor:
        if isinstance(object_, (list, dict, tuple)):
            return StructureConvertor()  # Возвращаем конвертер для структур

        for type_, converter_class in self._converters.items():
            if isinstance(object_, type_) or type_ is type(object_):
                return converter_class()  # Создаем экземпляр нужного конвертера

        raise ParamException(
            f"Impossible to create converter from object "
            f"with type '{type(object_).__name__}'"
        )

    def convert(self, object_: Any) -> Union[Dict, List]:
        converter = self.create(object_)
        return converter.convert(object_)