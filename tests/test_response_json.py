import json
import unittest
from src.core.exceptions import ParamException, WrongTypeException
from src.logics.response_json import ResponseJson
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils import get_properties


class TestResponseJson(unittest.TestCase):

    # Проверка формирования Json из модели группы номенклатуры
    def test_responsejson_build_create_json_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = ResponseJson()
        entity = NomenclatureGroupModel("test")
        data = [entity]
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
    
    # Проверка формирования Json из нескольких моделей единиц измерения
    def test_responsejson_build_create_json_from_measureunit_models_not_none(self):
        # Подготовка
        response = ResponseJson()
        data = [MeasureUnitModel(1, "гр"), MeasureUnitModel(1, "мл")]
        props = get_properties(MeasureUnitModel)
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
        
        obj = json.loads(result)
        assert obj is not None
        assert len(obj) == len(data)
    
    # Метод build() выбрасывает исключение при передаче пустого списка
    def test_responsejson_build_build_from_empty_list_raises_param_exception(self):
        # Подготовка
        response = ResponseJson()
        data = []
        # Действие и проверка
        with self.assertRaises(ParamException):
            response.build(data)

    # Метод build() выбрасывает исключение при передаче списка из моделей
    # разных типов
    def test_responsejson_build_build_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = ResponseJson()
        data = [MeasureUnitModel(1, "гр"), NomenclatureGroupModel("группа")]
        # Действие и проверка
        with self.assertRaises(WrongTypeException):
            response.build(data)


if __name__ == "__main__":
    unittest.main()
