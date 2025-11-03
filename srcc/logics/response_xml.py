from typing import Any, Dict, List, Union, Optional
from src.core.validator import Validator as vld
from src.core.exceptions import WrongTypeException
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.utils import obj_to_dict


"""Класс для формирования ответа в формате XML"""
class ResponseXml(AbstractResponse):
    
    def __init__(self):
        super().__init__()
    
    def build(self, data: List[Any]) -> str:
        super().build(data, ResponseFormat.XML)

        xml_head = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
        json = obj_to_dict(data)
        if len(json) == 1:
            json = json[0]

        return xml_head + "\n" + self.tag("root", json)

    """Возвращает XML тег"""
    def tag(
        self,
        name: str,
        content: Union[Dict, List, bool, int, float, str, None],
        list_name: Optional[str] = None,
    ) -> str:
        content = (self.get_content(content, list_name)
                   if content is not None
                   else "")
        return f"<{name}>{content}</{name}>"

    """Формирует из переданного объекта вложенный XML тег или строку"""
    def get_content(
        self,
        data: Union[Dict, List, bool, int, float, str],
        list_name: Optional[str] = None,
    ) -> str:
        if type(data) in [bool, int, float, str]:
            return str(data).strip()
        elif type(data) is dict:
            return "".join([self.tag(k, v, k) for k, v in data.items()])
        elif type(data) is list:
            item_name = self.get_list_item_name(list_name)
            return "".join([self.tag(item_name or f"{i}", item)
                            for i, item in enumerate(data)])
        else:
            raise WrongTypeException(
                f"Type of data must be in [Dict, List, bool, int, float, "
                f"str], but it's '{type(data).__name__}'"
            )
    
    """Возвращает имя элемента списка на основании названия списка"""
    def get_list_item_name(self, list_name: Optional[str]) -> Optional[str]:
        if list_name is None:
            return None
        return (list_name[:-1]
                if list_name.endswith("s") and len(list_name) > 1
                else list_name)
