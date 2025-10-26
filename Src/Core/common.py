from Src.Core.entity_model import entity_model
from Src.Core.abstract_model import abstact_model
from Src.Core.validator import argument_exception
from Src.Core.validator import operation_exception

class common:
    """
    Получить список наименований всех моделей
    """
    @staticmethod
    def get_models() -> list:
        result = []
        for inheritor in entity_model.__subclasses__():
            result.append(inheritor.__name__)
        return result    

    """
    Получить полный список полей любой модели
    """
    @staticmethod
    def get_fields(source) -> list:
        if source is None:
            raise operation_exception("Некорректно переданы аргументы!")

        # Проверяем, является ли source словарем (dict)
        if isinstance(source, dict):
            return list(source.keys())  # Возвращаем ключи словаря
        
        # Проверка, является ли source объектом класса
        if isinstance(source, (abstact_model, entity_model)):
            return [attr for attr in dir(source) 
                    if not attr.startswith('_') and not callable(getattr(source, attr))]

        raise operation_exception("Некорректный тип аргумента!")