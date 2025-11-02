import json
import unittest
from src.core.exceptions import ParamException, WrongTypeException
from src.logics.response_xml import ResponseXml
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils import get_properties


class TestResponseXml(unittest.TestCase):

    # Проверка формирования XML из модели группы номенклатуры
    def test_responsexml_build_create_xml_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = ResponseXml()
        entity = NomenclatureGroupModel("test")
        data = [entity]
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
    
    # Проверка формирования XML из нескольких моделей единиц измерения
    def test_responsexml_build_create_xml_from_measureunit_models_not_none(self):
        # Подготовка
        response = ResponseXml()
        data = [MeasureUnitModel(1, "гр"), MeasureUnitModel(1, "мл")]
        props = get_properties(MeasureUnitModel)
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
        
        assert result.startswith("<?xml")
    
    # Метод build() выбрасывает исключение при передаче пустого списка
    def test_responsexml_build_build_from_empty_list_raises_param_exception(self):
        # Подготовка
        response = ResponseXml()
        data = []
        # Действие и проверка
        with self.assertRaises(ParamException):
            response.build(data)

    # Метод build() выбрасывает исключение при передаче списка из моделей
    # разных типов
    def test_responsexml_build_build_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = ResponseXml()
        data = [MeasureUnitModel(1, "гр"), NomenclatureGroupModel("группа")]
        # Действие и проверка
        with self.assertRaises(WrongTypeException):
            response.build(data)


if __name__ == "__main__":
    unittest.main()
