import unittest
from src.core.exceptions import ParamException, WrongTypeException
from src.logics.response_markdown import ResponseMarkdown
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils import get_properties


class TestResponseMarkdown(unittest.TestCase):

    # Проверка формирования Markdown из модели группы номенклатуры
    def test_responsemarkdown_build_create_markdown_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = ResponseMarkdown()
        entity = NomenclatureGroupModel("test")
        data = [entity]
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
    
    # Проверка формирования Markdown из нескольких моделей единиц измерения
    def test_responsemarkdown_build_create_markdown_from_measureunit_models_not_none(self):
        # Подготовка
        response = ResponseMarkdown()
        data = [MeasureUnitModel(1, "гр"), MeasureUnitModel(1, "мл")]
        props = get_properties(MeasureUnitModel)
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
        
        headers_3 = result.count("### ")
        headers_2 = result.count("## ") - headers_3
        headers_1 = result.count("# ") - headers_3 - headers_2

        assert headers_1 == 1
        assert headers_2 == len(data)
        assert headers_3 == len(data) * len(props)
    
    # Метод build() выбрасывает исключение при передаче пустого списка
    def test_responsemarkdown_build_build_from_empty_list_raises_param_exception(self):
        # Подготовка
        response = ResponseMarkdown()
        data = []
        # Действие и проверка
        with self.assertRaises(ParamException):
            response.build(data)

    # Метод build() выбрасывает исключение при передаче списка из моделей
    # разных типов
    def test_responsemarkdown_build_build_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = ResponseMarkdown()
        data = [MeasureUnitModel(1, "гр"), NomenclatureGroupModel("группа")]
        # Действие и проверка
        with self.assertRaises(WrongTypeException):
            response.build(data)


if __name__ == "__main__":
    unittest.main()
